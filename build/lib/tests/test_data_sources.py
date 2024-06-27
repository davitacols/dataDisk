import unittest
import pandas as pd
from io import StringIO
from unittest.mock import patch, mock_open
from dataDisk.data_sources import CSVDataSource, SQLDataSource

class TestCSVDataSource(unittest.TestCase):

    @patch('dat_sourceS.pd.read_csv')
    def test_read_from_local_file(self, mock_read_csv):
        # Mock the return value of pd.read_csv
        mock_read_csv.return_value = pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']})
        csv_source = CSVDataSource('data.csv')
        result = csv_source.read()
        mock_read_csv.assert_called_once_with('data.csv')
        pd.testing.assert_frame_equal(result, pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']}))

    @patch('dat_sourceS.pd.read_csv')
    def test_read_from_url(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']})
        csv_source = CSVDataSource('https://example.com/data.csv')
        result = csv_source.read()
        mock_read_csv.assert_called_once_with('https://example.com/data.csv')
        pd.testing.assert_frame_equal(result, pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']}))

    @patch('builtins.open', new_callable=mock_open)
    @patch('dat_sourceS.pd.DataFrame.to_csv')
    def test_write_to_local_file(self, mock_to_csv, mock_open_file):
        data = pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']})
        csv_source = CSVDataSource('data.csv')
        csv_source.write(data)
        mock_to_csv.assert_called_once_with('data.csv', index=False)

    def test_write_to_url_raises_error(self):
        data = pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']})
        csv_source = CSVDataSource('https://example.com/data.csv')
        with self.assertRaises(ValueError):
            csv_source.write(data)


class TestSQLDataSource(unittest.TestCase):

    @patch('dat_sourceS.sqlite3.connect')
    def test_read(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = [(1, 'a'), (2, 'b')]
        sql_source = SQLDataSource('db.sqlite')
        sql_source.read()
        mock_connect.assert_called_once_with('db.sqlite')
        mock_conn.close.assert_called_once()

    @patch('dat_sourceS.sqlite3.connect')
    def test_write(self, mock_connect):
        mock_conn = mock_connect.return_value
        data = pd.DataFrame({'column1': [1, 2], 'column2': ['a', 'b']})
        sql_source = SQLDataSource('db.sqlite')
        sql_source.write(data)
        mock_connect.assert_called_once_with('db.sqlite')
        mock_conn.close.assert_called_once()
        self.assertTrue(mock_conn.__enter__.return_value.cursor.return_value.execute.called)

if __name__ == '__main__':
    unittest.main()
