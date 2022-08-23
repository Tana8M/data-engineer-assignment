from api import delisted_company_api, history_dividends_api
from postgresql_function import psycopg2_postgresql
import pandas as pd
import pandera as p
import dagster


''' 
Transform validation delisted_company 
'''

df_company = pd.json_normalize(delisted_company_api.get_jsonparsed_data_delisted_company(api_key='10c0c76dfaabef8d2ba52d1fb7e5bf8d'))
df_company.to_csv('list.csv')
print(df_company)
