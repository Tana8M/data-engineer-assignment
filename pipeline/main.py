from api.history_dividends_api import get_jsonparsed_data_history_dividends
from api.delisted_company_api import get_jsonparsed_data_delisted_company
from function.postgresql_function.psycopg2_postgresql import *
from function.slack_notify import *
from function.validation.validation_json_api import json_validation_history_dividends, json_validation_delisted_company
import pandas as pd
import numpy as np
from dagster import op, job
import os
from dagster_slack import slack_resource

api_key = os.environ['API_KEY']


@op(description='Request Data from delisted company api', required_resource_keys={'slack'})
def delisted_company_json_data():
    data_json = get_jsonparsed_data_delisted_company(api_key=api_key)
    return data_json


@op(description='Request Data from history_dividends api', required_resource_keys={'slack'})
def history_dividends_json_data(symbol):
    data_json = get_jsonparsed_data_history_dividends(symbol=symbol, api_key=api_key)
    return data_json


@op(description='Validation history dividends json', required_resource_keys={'slack'})
def validation_history_dividends_json(json):
    data_json = json_validation_history_dividends(json)
    return data_json


@op(description='Validation delisted company json', required_resource_keys={'slack'})
def validation_delisted_company_json(json):
    data_json = json_validation_delisted_company(json)
    return data_json


@op(description='Transform json to DataFrame history_dividends', required_resource_keys={'slack'})
def transform_json_to_dataframe_history_dividends(df):
    data = []
    df = df['symbol'].head(4)
    for index, value in df.items():
        data_json = validation_history_dividends_json(history_dividends_json_data(symbol=value))
        try:
            df_history = pd.json_normalize(data_json, record_path=['historical'], meta=['symbol'])
        except KeyError as er:
            print(er)
            pass
        data.append(df_history)
    return pd.concat(data)


@op(description='Transform json to DataFrame history_dividends', required_resource_keys={'slack'})
def transform_json_to_dataframe_delisted_company(data_json):
    df = pd.json_normalize(data_json)
    return df


@op(description='Loading DataFrame to Postgresql Table delisted_company', required_resource_keys={'slack'})
def loading_dataframe_to_database_delisted_company(df):
    conn = PsycopgPostgresWarehouse(
        host=os.environ['PROD_HOST'],
        database=os.environ['PROD_DATABASE'],
        user=os.environ['PROD_USER'],
        pw=os.environ['PROD_PW'],
        port=os.environ['PROD_PORT']
    ).connect_database()

    PsycopgPostgresWarehouse.execute_mogrify_upsert(conn=conn, dataframe=df, column_unique='symbol',
                                                    table='delisted_company')
    print(df)


@op(description='Loading DataFrame to Postgresql Table history dividend', required_resource_keys={'slack'})
def loading_dataframe_to_database_history_dividends(df):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.where(pd.notnull(df), None)
    conn = PsycopgPostgresWarehouse(
        host=os.environ['PROD_HOST'],
        database=os.environ['PROD_DATABASE'],
        user=os.environ['PROD_USER'],
        pw=os.environ['PROD_PW'],
        port=os.environ['PROD_PORT']
    ).connect_database()

    PsycopgPostgresWarehouse.execute_mogrify_insert(conn=conn, dataframe=df, table='history_dividends')
    print(df)


@job(resource_defs={"slack": slack_resource}, hooks={slack_message_on_failure})
def etl_pipline():
    json_company = delisted_company_json_data()
    json_validate_company = validation_delisted_company_json(json=json_company)
    df_company = transform_json_to_dataframe_delisted_company(data_json=json_validate_company)
    df_dividends = transform_json_to_dataframe_history_dividends(df=df_company)
    loading_dataframe_to_database_delisted_company(df_company)
    loading_dataframe_to_database_history_dividends.with_hooks({slack_message_on_success})(df_dividends)


if __name__ == "__main__":
    result = etl_pipline.execute_in_process(raise_on_error=False,
                                            run_config={
                                                'resources': {'slack': {
                                                    'config': {
                                                        'token': os.environ['SLACK_BOT_API']}}}}
                                            )
