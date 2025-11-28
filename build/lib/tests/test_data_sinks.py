import logging
import os
import pandas as pd
import pytest
import sqlite3
import tempfile
from dataDisk.data_sinks import (
    CSVSink, JSONSink, SQLSink, ExcelSink, ParquetSink, MultiSink
)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create sample data
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [6, 7, 8, 9, 10],
        'category': ['A', 'B', 'A', 'B', 'A'],
        'feature3': [None, 2, None, 4, 5]
    })


# Define file paths using pytest fixtures for cleanup
@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def file_paths(temp_dir):
    return {
        'csv': os.path.join(temp_dir, 'test_output.csv'),
        'json': os.path.join(temp_dir, 'test_output.json'),
        'db': os.path.join(temp_dir, 'test_output.db'),
        'excel': os.path.join(temp_dir, 'test_output.xlsx'),
        'parquet': os.path.join(temp_dir, 'test_output.parquet')
    }


# Test CSVSink
def test_csv_sink(sample_data, file_paths):
    csv_sink = CSVSink(file_paths['csv'])
    result = csv_sink.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['csv'])
    
    # Verify data
    loaded_data = pd.read_csv(file_paths['csv'])
    assert len(loaded_data) == len(sample_data)
    assert all(col in loaded_data.columns for col in sample_data.columns)


# Test CSVSink with custom parameters
def test_csv_sink_with_params(sample_data, file_paths):
    csv_sink = CSVSink(file_paths['csv'], sep='|', index=True)
    csv_sink.save(sample_data)
    
    # Verify data with custom separator
    loaded_data = pd.read_csv(file_paths['csv'], sep='|')
    assert len(loaded_data) == len(sample_data)


# Test JSONSink
def test_json_sink(sample_data, file_paths):
    json_sink = JSONSink(file_paths['json'])
    result = json_sink.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['json'])
    
    # Verify data
    loaded_data = pd.read_json(file_paths['json'], orient='records')
    assert len(loaded_data) == len(sample_data)


# Test JSONSink with custom parameters
def test_json_sink_with_params(sample_data, file_paths):
    json_sink = JSONSink(file_paths['json'], orient='split')
    json_sink.save(sample_data)
    
    # Verify data with custom orientation
    loaded_data = pd.read_json(file_paths['json'], orient='split')
    assert len(loaded_data) == len(sample_data)


# Test SQLSink
def test_sql_sink(sample_data, file_paths):
    table_name = 'test_table'
    sql_sink = SQLSink(file_paths['db'], table_name)
    result = sql_sink.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['db'])
    
    # Verify data in SQLite database
    conn = sqlite3.connect(file_paths['db'])
    retrieved_data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    
    assert not retrieved_data.empty
    assert len(retrieved_data) == len(sample_data)


# Test SQLSink with append mode
def test_sql_sink_append(sample_data, file_paths):
    table_name = 'test_table'
    
    # First save
    sql_sink = SQLSink(file_paths['db'], table_name)
    sql_sink.save(sample_data)
    
    # Second save with append
    sql_sink_append = SQLSink(file_paths['db'], table_name, if_exists='append')
    sql_sink_append.save(sample_data)
    
    # Verify data is doubled
    conn = sqlite3.connect(file_paths['db'])
    retrieved_data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    
    assert len(retrieved_data) == len(sample_data) * 2


# Test ExcelSink
def test_excel_sink(sample_data, file_paths):
    excel_sink = ExcelSink(file_paths['excel'])
    result = excel_sink.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['excel'])
    
    # Verify data
    loaded_data = pd.read_excel(file_paths['excel'])
    assert len(loaded_data) == len(sample_data)


# Test ExcelSink with custom sheet name
def test_excel_sink_with_sheet(sample_data, file_paths):
    sheet_name = 'TestSheet'
    excel_sink = ExcelSink(file_paths['excel'], sheet_name=sheet_name)
    excel_sink.save(sample_data)
    
    # Verify data with custom sheet name
    loaded_data = pd.read_excel(file_paths['excel'], sheet_name=sheet_name)
    assert len(loaded_data) == len(sample_data)


# Test ParquetSink
def test_parquet_sink(sample_data, file_paths):
    try:
        parquet_sink = ParquetSink(file_paths['parquet'])
        result = parquet_sink.save(sample_data)
        
        assert result is True
        assert os.path.exists(file_paths['parquet'])
        
        # Verify data
        loaded_data = pd.read_parquet(file_paths['parquet'])
        assert len(loaded_data) == len(sample_data)
    except ImportError:
        pytest.skip("pyarrow or fastparquet not installed")


# Test MultiSink
def test_multi_sink(sample_data, file_paths):
    sinks = [
        CSVSink(file_paths['csv']),
        JSONSink(file_paths['json']),
        SQLSink(file_paths['db'], 'test_table')
    ]
    
    multi_sink = MultiSink(sinks)
    result = multi_sink.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['csv'])
    assert os.path.exists(file_paths['json'])
    assert os.path.exists(file_paths['db'])


# Test MultiSink with error handling
def test_multi_sink_with_error(sample_data, file_paths, monkeypatch):
    # Create a sink that will fail
    class FailingSink(CSVSink):
        def save(self, data):
            raise ValueError("Simulated failure")
    
    sinks = [
        CSVSink(file_paths['csv']),
        FailingSink("nonexistent/path.csv")
    ]
    
    multi_sink = MultiSink(sinks)
    
    with pytest.raises(Exception):
        multi_sink.save(sample_data)
    
    # First sink should still have worked
    assert os.path.exists(file_paths['csv'])
