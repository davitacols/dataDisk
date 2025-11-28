"""
Examples demonstrating the use of various data sources in dataDisk.
"""

import pandas as pd
import os
import sqlite3
from dataDisk.data_sources import (
    CSVDataSource, SQLDataSource, JSONDataSource, ExcelDataSource, ParquetDataSource
)

# Create sample data
data = pd.DataFrame({
    'id': range(1, 6),
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 40, 45],
    'score': [95.5, 85.0, 88.5, 92.0, 78.5]
})

print("Sample data:")
print(data)
print("\n")

# Example 1: Basic CSV source
print("Example 1: Using CSV data source")
csv_source = CSVDataSource('data_source_output.csv')
csv_source.save(data)
print("Data saved to CSV file")

# Load the data back
loaded_csv = csv_source.load()
print("Data loaded from CSV file:")
print(loaded_csv.head())
print("\n")

# Example 2: JSON source with different orientations
print("Example 2: Using JSON data source with different orientations")
json_source1 = JSONDataSource('data_source_records.json', orient='records')
json_source1.save(data)
print("Data saved as records to JSON file")

json_source2 = JSONDataSource('data_source_table.json', orient='table')
json_source2.save(data)
print("Data saved as table to JSON file")

# Load the data back
loaded_json = json_source1.load()
print("Data loaded from JSON file:")
print(loaded_json.head())
print("\n")

# Example 3: SQLite source
print("Example 3: Using SQL data source")
db_file = 'data_source_database.db'
sql_source = SQLDataSource(db_file, 'people')
sql_source.save(data)
print("Data saved to SQLite database")

# Load the data back
loaded_sql = sql_source.load()
print("Data loaded from SQLite database:")
print(loaded_sql.head())

# Load with custom query
custom_query = "SELECT name, age FROM people WHERE age > 30"
filtered_data = sql_source.load(custom_query)
print("Data loaded with custom query:")
print(filtered_data)
print("\n")

# Example 4: Excel source with multiple sheets
print("Example 4: Using Excel data source")
excel_file = 'data_source_excel.xlsx'
excel_source1 = ExcelDataSource(excel_file, sheet_name='Raw Data')
excel_source1.save(data)
print("Data saved to Excel file")

# Create a modified version of the data for a second sheet
data_summary = pd.DataFrame({
    'metric': ['count', 'mean_age', 'mean_score'],
    'value': [len(data), data['age'].mean(), data['score'].mean()]
})

excel_source2 = ExcelDataSource(excel_file, sheet_name='Summary', mode='a')
excel_source2.save(data_summary)
print("Summary data saved to second sheet")

# Load the data back
loaded_excel = excel_source1.load()
print("Data loaded from Excel file:")
print(loaded_excel.head())
print("\n")

# Example 5: Parquet source
try:
    print("Example 5: Using Parquet data source")
    parquet_file = 'data_source_data.parquet'
    parquet_source = ParquetDataSource(parquet_file)
    parquet_source.save(data)
    print("Data saved to Parquet file")
    
    # Load the data back
    loaded_parquet = parquet_source.load()
    print("Data loaded from Parquet file:")
    print(loaded_parquet.head())
    print("\n")
except ImportError:
    print("Parquet example skipped: pyarrow or fastparquet not installed\n")

print("All examples completed. Output files created in the current directory.")