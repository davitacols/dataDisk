import os
import pandas as pd
import pytest
import sqlite3
import tempfile
from dataDisk.data_sources import (
    CSVDataSource, SQLDataSource, JSONDataSource, ExcelDataSource, ParquetDataSource
)


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
        'csv': os.path.join(temp_dir, 'test_data.csv'),
        'json': os.path.join(temp_dir, 'test_data.json'),
        'db': os.path.join(temp_dir, 'test_data.db'),
        'excel': os.path.join(temp_dir, 'test_data.xlsx'),
        'parquet': os.path.join(temp_dir, 'test_data.parquet')
    }


# Test CSVDataSource
def test_csv_source(sample_data, file_paths):
    # Save data
    csv_source = CSVDataSource(file_paths['csv'])
    result = csv_source.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['csv'])
    
    # Load data
    loaded_data = csv_source.load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test CSVDataSource with custom parameters
def test_csv_source_with_params(sample_data, file_paths):
    # Save with custom separator
    csv_source = CSVDataSource(file_paths['csv'], sep='|')
    csv_source.save(sample_data)
    
    # Load with custom separator
    loaded_data = CSVDataSource(file_paths['csv'], sep='|').load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test SQLDataSource
def test_sql_source(sample_data, file_paths):
    table_name = 'test_table'
    
    # Save data
    sql_source = SQLDataSource(file_paths['db'], table_name)
    result = sql_source.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['db'])
    
    # Load data
    loaded_data = sql_source.load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test SQLDataSource with custom query
def test_sql_source_with_query(sample_data, file_paths):
    table_name = 'test_table'
    
    # Save data
    sql_source = SQLDataSource(file_paths['db'], table_name)
    sql_source.save(sample_data)
    
    # Load with custom query
    query = f"SELECT feature1, feature2 FROM {table_name} WHERE feature1 > 2"
    loaded_data = sql_source.load(query)
    
    expected = sample_data[sample_data['feature1'] > 2][['feature1', 'feature2']]
    pd.testing.assert_frame_equal(loaded_data, expected)


# Test JSONDataSource
def test_json_source(sample_data, file_paths):
    # Save data
    json_source = JSONDataSource(file_paths['json'])
    result = json_source.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['json'])
    
    # Load data
    loaded_data = json_source.load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test JSONDataSource with custom orientation
def test_json_source_with_orientation(sample_data, file_paths):
    # Save with split orientation
    json_source = JSONDataSource(file_paths['json'], orient='split')
    json_source.save(sample_data)
    
    # Load with split orientation
    loaded_data = JSONDataSource(file_paths['json'], orient='split').load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test ExcelDataSource
def test_excel_source(sample_data, file_paths):
    # Save data
    excel_source = ExcelDataSource(file_paths['excel'])
    result = excel_source.save(sample_data)
    
    assert result is True
    assert os.path.exists(file_paths['excel'])
    
    # Load data
    loaded_data = excel_source.load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test ExcelDataSource with custom sheet name
def test_excel_source_with_sheet(sample_data, file_paths):
    sheet_name = 'TestSheet'
    
    # Save with custom sheet
    excel_source = ExcelDataSource(file_paths['excel'], sheet_name=sheet_name)
    excel_source.save(sample_data)
    
    # Load with custom sheet
    loaded_data = ExcelDataSource(file_paths['excel'], sheet_name=sheet_name).load()
    pd.testing.assert_frame_equal(loaded_data, sample_data)


# Test ParquetDataSource
def test_parquet_source(sample_data, file_paths):
    try:
        # Save data
        parquet_source = ParquetDataSource(file_paths['parquet'])
        result = parquet_source.save(sample_data)
        
        assert result is True
        assert os.path.exists(file_paths['parquet'])
        
        # Load data
        loaded_data = parquet_source.load()
        pd.testing.assert_frame_equal(loaded_data, sample_data)
    except ImportError:
        pytest.skip("pyarrow or fastparquet not installed")


# Test error handling
def test_csv_source_file_not_found():
    csv_source = CSVDataSource('nonexistent_file.csv')
    with pytest.raises(FileNotFoundError):
        csv_source.load()


# Test multiple data sources with the same data
def test_multiple_sources(sample_data, file_paths):
    # Save to different formats
    sources = [
        CSVDataSource(file_paths['csv']),
        JSONDataSource(file_paths['json']),
        SQLDataSource(file_paths['db'], 'test_table'),
        ExcelDataSource(file_paths['excel'])
    ]
    
    # Save data using each source
    for source in sources:
        source.save(sample_data)
    
    # Load data from each source and verify
    for source in sources:
        loaded_data = source.load()
        pd.testing.assert_frame_equal(loaded_data, sample_data)