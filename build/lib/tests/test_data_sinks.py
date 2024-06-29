import logging
import os
import pandas as pd
from dataDisk.data_sinks import CSVSink, JSONSink, SQLSink


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create sample data
sample_data = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [6, 7, 8, 9, 10],
    'category': ['A', 'B', 'A', 'B', 'A'],
    'feature3': [None, 2, None, 4, 5]
})

# Define file paths
csv_file_path = 'test_output.csv'
json_file_path = 'test_output.json'
db_file_path = 'test_output.db'
table_name = 'test_table'


# Test CSVSink
def test_csv_sink():
    try:
        csv_sink = CSVSink(csv_file_path)
        csv_sink.save(sample_data)
        logging.info(f"CSV data saved to {csv_file_path}")
        assert os.path.exists(csv_file_path)
    except Exception as e:
        logging.error(f"Error during CSV sink test: {str(e)}")


# Test JSONSink
def test_json_sink():
    try:
        json_sink = JSONSink(json_file_path)
        json_sink.save(sample_data)
        logging.info(f"JSON data saved to {json_file_path}")
        assert os.path.exists(json_file_path)
    except Exception as e:
        logging.error(f"Error during JSON sink test: {str(e)}")


# Test SQLSink
def test_sql_sink():
    try:
        sql_sink = SQLSink(db_file_path, table_name)
        sql_sink.save(sample_data)
        logging.info(f"SQLite data saved to {db_file_path}, table {table_name}")

        # Verify data in SQLite database
        conn = sqlite3.connect(db_file_path)
        retrieved_data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        assert not retrieved_data.empty
    except Exception as e:
        logging.error(f"Error during SQL sink test: {str(e)}")


# Run tests
if __name__ == '__main__':
    test_csv_sink()
    test_json_sink()
    test_sql_sink()

    # Cleanup files
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    if os.path.exists(db_file_path):
        os.remove(db_file_path)

    logging.info("All tests completed.")
