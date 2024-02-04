# data_sources.py

import pyarrow
import pandas as pd
import sqlalchemy


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

    def __init__(self, connection_uri):
        self.connection_uri = connection_uri

    def get_connection(self):
        return sqlalchemy.create_engine(self.connection_uri) 

    def read(self):
        with self.get_connection() as conn:
            return pd.read_sql(conn)

    def write(self, data):
        with self.get_connection() as conn:
            data.to_sql('results', conn, if_exists='replace')


if __name__ == '__main__':

    # Examples 
    csv_source = CSVDataSource('data.csv')
    sql_source = SQLDataSource('sqlite:///db.sqlite')
