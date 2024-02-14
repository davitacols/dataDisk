# data_sources.py
import pandas as pd
import sqlite3

class DataSource:

    def read(self):
        raise NotImplementedError
    
    def write(self, data):
        raise NotImplementedError


class CSVDataSource(DataSource):

    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        return pd.read_csv(self.filepath)

    def write(self, data):
        data.to_csv(self.filepath, index=False)


class SQLDataSource(DataSource):

    def __init__(self, db_filepath, table_name='results'):
        self.db_filepath = db_filepath
        self.table_name = table_name

    def read(self, query='SELECT * FROM '):
        conn = sqlite3.connect(self.db_filepath)
        try:
            return pd.read_sql_query(query + self.table_name, conn)
        finally:
            conn.close()

    def write(self, data):
        conn = sqlite3.connect(self.db_filepath)
        try:
            data.to_sql(self.table_name, conn, if_exists='replace', index=False)
        finally:
            conn.close()


if __name__ == '__main__':

    # Examples 
    csv_source = CSVDataSource('data.csv')
    sql_source = SQLDataSource('db.sqlite')

    # Reading from SQL source
    sql_data = sql_source.read()
    print(sql_data)

    # Writing to SQL source
    data_to_write = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    sql_source.write(data_to_write)
