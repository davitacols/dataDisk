import os
import sqlite3
import pandas as pd
import unittest
import pytest
from dataDisk.data_sources import CSVDataSource, SQLDataSource

# Test data
TEST_CSV_FILE = 'test_data.csv'
TEST_SQL_FILE = 'test_db.sqlite'
TEST_SQL_TABLE = 'test_table'


@pytest.fixture(scope='module')
def setup_csv_data():
    # Create test CSV file
    data = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
    data.to_csv(TEST_CSV_FILE, index=False)
    yield
    # Clean up
    os.remove(TEST_CSV_FILE)


@pytest.fixture(scope='module')
def setup_sql_data():
    # Create test SQL database and table
    conn = sqlite3.connect(TEST_SQL_FILE)
    data = pd.DataFrame({'A': [4, 5, 6], 'B': ['d', 'e', 'f']})
    data.to_sql(TEST_SQL_TABLE, conn, if_exists='replace', index=False)
    conn.close()
    yield
    # Clean up
    os.remove(TEST_SQL_FILE)


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
    # Run unittest
    unittest.main()

    # Run pytest
    pytest.main([__file__])
