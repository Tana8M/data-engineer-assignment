import psycopg2 as psy
import pandas as pd


# Class for connect and write Postgresql
class PsycopgPostgresWarehouse:

    def __init__(self, host, database, user, pw, port):
        self.host = host
        self.database = database
        self.user = user
        self.pw = pw
        self.port = port

    # Connect Database
    def connect_database(self) -> str:

        try:
            conn = psy.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.pw,
                port=self.port
            )
            print("Connect Success")

        except:
            print("Failed connect")

        return conn

    # Connect database query data to Dataframe
    @staticmethod
    def to_dataframe(conn, query) -> pd.DataFrame:
        df = pd.read_sql(query, conn)
        return df

    # https://www.mindphp.com/developer/tips-python/7907-static-method-in-python.html#:~:text=Static
    # %20method%20%E0%B8%84%E0%B8%B7%E0%B8%AD%20%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%97%E0%B8%B3%E0%B9%83%E0%B8%AB%E0%B9
    # %89,%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%81%E0%B9%80%E0%B8%A1%E0%B8%98%E0%B8%AD%E0%B8%94%E0%B9%81%E0%B8
    # %95%E0%B9%88%E0%B8%A5%E0%B8%B0%E0%B8%84%E0%B8%A3%E0%B8%B1%E0%B9%89%E0%B8%87%20%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8
    # %99
    @staticmethod
    def execute_mogrify_upsert(conn, dataframe, column_unique, table):
        df_not_unique_key = dataframe.drop(columns=column_unique)
        upsert_value = ["EXCLUDED." + s for s in df_not_unique_key.columns]

        tpls = [tuple(x) for x in dataframe.to_numpy()]
        cols = ','.join(list(dataframe.columns))
        cols_2 = ','.join(list(df_not_unique_key.columns))
        cols_3 = ','.join(upsert_value)
        no_column = len(dataframe.columns)
        add_no_column_to_insert = "%s," * no_column
        add = add_no_column_to_insert.rstrip(add_no_column_to_insert[-1])
        cursor = conn.cursor()
        values = [cursor.mogrify("(" + add + ")", tup).decode('utf8') for tup in tpls]
        sql = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(
            values) + " ON CONFLICT (" + column_unique + ") DO UPDATE SET (" + cols_2 + ")" + " = (" + cols_3 + ")"
        # print(sql)
        cursor.execute(sql)
        print("Data upserted using execute_mogrify() successfully. : " + str(table) + "")
        conn.commit()
        cursor.close()

    @staticmethod
    def execute_mogrify_upsert_single_column(conn, dataframe, column_unique, table):
        df_not_unique_key = dataframe.drop(columns=column_unique)
        upsert_value = ["EXCLUDED." + s for s in df_not_unique_key.columns]

        tpls = [tuple(x) for x in dataframe.to_numpy()]
        cols = ','.join(list(dataframe.columns))
        cols_2 = ','.join(list(df_not_unique_key.columns))
        cols_3 = ','.join(upsert_value)
        no_column = len(dataframe.columns)
        add_no_column_to_insert = "%s," * no_column
        add = add_no_column_to_insert.rstrip(add_no_column_to_insert[-1])
        cursor = conn.cursor()
        values = [cursor.mogrify("(" + add + ")", tup).decode('utf8') for tup in tpls]
        sql = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(
            values) + " ON CONFLICT (" + column_unique + ") DO UPDATE SET " + cols_2 + "" + " = " + cols_3 + ""
        # print(function)
        cursor.execute(sql)
        print("Data upserted using execute_mogrify() successfully. : " + str(table) + "")
        conn.commit()
        cursor.close()

    @staticmethod
    def execute_mogrify_insert(conn, dataframe, table):
        # Creating a list of tupples from the dataframe values
        tpls = [tuple(x) for x in dataframe.to_numpy()]

        # dataframe columns with Comma-separated
        cols = ','.join(list(dataframe.columns))
        no_column = len(dataframe.columns)
        add_no_column_to_insert = "%s," * no_column
        add = add_no_column_to_insert.rstrip(add_no_column_to_insert[-1])
        # SQL query to execute
        cursor = conn.cursor()
        values = [cursor.mogrify("(" + add + ")", tup).decode('utf8') for tup in tpls]
        sql = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(values)
        # print(function)
        try:
            cursor.execute(sql)
            # print(cursor.execute(function))
            conn.commit()
            print("Data inserted using execute_mogrify() successfully.")
            cursor.close()
        except (Exception, psy.DatabaseError):
            print(psy.DatabaseError)
            print("Error")
            cursor.close()
            pass
