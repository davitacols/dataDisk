import unittest
import pandas as pd
import sqlite3
import os

from dataDisk.data_sources import CSVDataSource, SQLDataSource

class TestDataSources(unittest.TestCase):

    def setUp(self):
        self.csv_filepath = 'test.csv'
        self.sql_db_filepath = 'test.db'
        self.data = pd.DataFrame({'col1': [1, 2]})

    def tearDown(self):
        if os.path.exists(self.csv_filepath):
            os.remove(self.csv_filepath)
        if os.path.exists(self.sql_db_filepath):
            os.remove(self.sql_db_filepath)

    def test_csv_read_write(self):
        # Test CSVDataSource read and write
        csv_source = CSVDataSource(self.csv_filepath)

        # Write data to CSV
        csv_source.write(self.data)

        # Read data from CSV
        data_out = csv_source.read()

        # Assert data equality
        pd.testing.assert_frame_equal(self.data, data_out)

    def test_sql_read_write(self):
        # Test SQLDataSource read and write
        with sqlite3.connect(self.sql_db_filepath) as conn:
            # Create test table and insert data
            self.data.to_sql('test_table', conn, index=False)

        sql_source = SQLDataSource(self.sql_db_filepath, table_name='test_table')

        # Read data from SQL
        data_out = sql_source.read()

        # Assert data equality
        pd.testing.assert_frame_equal(self.data, data_out)

        # Write data to SQL
        new_data = pd.DataFrame({'col1': [3, 4]})
        sql_source.write(new_data)

        # Read updated data from SQL
        updated_data_out = pd.read_sql_query('SELECT * FROM test_table', sqlite3.connect(self.sql_db_filepath))

        # Assert updated data equality
        pd.testing.assert_frame_equal(new_data, updated_data_out)

if __name__ == '__main__':
    unittest.main()
