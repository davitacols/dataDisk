import pandas as pd
import logging
import sqlite3


class DataSource:
    def load(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def save(self, data):
        raise NotImplementedError("Subclasses should implement this method.")


class CSVDataSource(DataSource):
    def __init__(self, file_path, sep=','):
        self.file_path = file_path
        self.sep = sep

    def load(self):
        logging.info(f"Loading data from {self.file_path}")
        data = pd.read_csv(self.file_path, sep=self.sep)
        return data

    def save(self, data):
        logging.info(f"Saving data to {self.file_path}")
        data.to_csv(self.file_path, sep=self.sep, index=False)


class SQLDataSource(DataSource):
    def __init__(self, db_filepath, table_name='results'):
        self.db_filepath = db_filepath
        self.table_name = table_name

    def load(self, query=None):
        if query is None:
            query = f"SELECT * FROM {self.table_name}"
        conn = sqlite3.connect(self.db_filepath)
        try:
            return pd.read_sql_query(query, conn)
        finally:
            conn.close()

    def save(self, data):
        conn = sqlite3.connect(self.db_filepath)
        try:
            data.to_sql(self.table_name, conn, if_exists='replace', index=False)
        finally:
            conn.close()


if __name__ == '__main__':
    # Examples
    csv_source = CSVDataSource('data.csv')
    sql_source = SQLDataSource('db.sqlite')

    # Reading from a local CSV file
    csv_data = csv_source.load()
    print(csv_data)

    # Reading from SQL source
    sql_data = sql_source.load()
    print(sql_data)

    # Writing to SQL source
    data_to_write = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    sql_source.save(data_to_write)
