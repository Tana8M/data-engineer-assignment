from api.delisted_company_api import get_jsonparsed_data_delisted_company
from api.history_dividends_api import get_jsonparsed_data_history_dividends
from job.validation.validation_json_api import json_validation_history_dividends, json_validation_delisted_company
from postgresql_function import psycopg2_postgresql
import pandas as pd
import pandera as p
import dagster

''' 
Transform delist_company and history dividends
'''

# json_validation_history_dividends(get_jsonparsed_data_history_dividends(symbol='AAL', api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'))
# json_validation_delisted_company(get_jsonparsed_data_delisted_company(api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'))
# print(delisted_company_api.get_jsonparsed_data_delisted_company(api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'))
# print(history_dividends_api.get_jsonparsed_data_history_dividends(symbol='AAL', api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'))
# df_company = pd.json_normalize(get_jsonparsed_data_delisted_company(api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'))
# df_company.to_csv('list.csv',index=False)
df = pd.read_csv('list.csv', index_col=None)
df = df['symbol'].head(4)
data = []
for index, value in df.items():
    data_json = get_jsonparsed_data_history_dividends(symbol=value, api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d')
    try:
        dataframe = pd.json_normalize(data_json, record_path=['historical'], meta=['symbol'])
    except KeyError as er:
        print(er)
        pass
    data.append(dataframe)
result = pd.concat(data)
result.to_csv('data.csv', index=False)
print(df)
# df_history_dividends = pd.json_normalize(get_jsonparsed_data_history_dividends(symbol='AAL', api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'),record_path =['historical'], meta=['symbol'])
# df_history_dividends.to_csv('dividend2.csv')
# df_company.to_json('test.json')
