import logging
import pandas as pd
import sqlite3

class DataSink:
    def save(self, data):
        raise NotImplementedError("Subclasses must implement this method")


class CSVSink(DataSink):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data):
        try:
            logging.info(f"Saving data to {self.file_path}")
            data.to_csv(self.file_path, index=False)
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data to CSV: {str(e)}")
            raise


class JSONSink(DataSink):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data):
        try:
            logging.info(f"Saving data to {self.file_path}")
            data.to_json(self.file_path, orient='records', lines=True)
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data to JSON: {str(e)}")
            raise


class SQLSink(DataSink):
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name

    def save(self, data):
        try:
            logging.info(f"Saving data to SQLite database {self.db_path}, table {self.table_name}")
            conn = sqlite3.connect(self.db_path)
            data.to_sql(self.table_name, conn, if_exists='replace', index=False)
            conn.close()
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data to SQLite: {str(e)}")
            raise
