"""
Examples demonstrating the use of various data sinks in dataDisk.
"""

import pandas as pd
import os
from dataDisk.data_sinks import (
    CSVSink, JSONSink, SQLSink, ExcelSink, ParquetSink, MultiSink
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

# Example 1: Basic CSV sink
print("Example 1: Saving to CSV")
csv_sink = CSVSink('output_data.csv')
csv_sink.save(data)
print("Data saved to output_data.csv\n")

# Example 2: JSON sink with different orientations
print("Example 2: Saving to JSON with different orientations")
json_sink1 = JSONSink('output_records.json', orient='records')
json_sink1.save(data)
print("Data saved as records to output_records.json")

json_sink2 = JSONSink('output_table.json', orient='table')
json_sink2.save(data)
print("Data saved as table to output_table.json\n")

# Example 3: SQLite sink
print("Example 3: Saving to SQLite database")
sql_sink = SQLSink('output_database.db', 'people')
sql_sink.save(data)
print("Data saved to SQLite database output_database.db in table 'people'\n")

# Example 4: Excel sink with multiple sheets
print("Example 4: Saving to Excel with multiple sheets")
excel_sink1 = ExcelSink('output_data.xlsx', sheet_name='Raw Data')
excel_sink1.save(data)

# Create a modified version of the data for a second sheet
data_summary = pd.DataFrame({
    'metric': ['count', 'mean_age', 'mean_score'],
    'value': [len(data), data['age'].mean(), data['score'].mean()]
})

excel_sink2 = ExcelSink('output_data.xlsx', sheet_name='Summary', mode='a')
excel_sink2.save(data_summary)
print("Data saved to Excel file output_data.xlsx with multiple sheets\n")

# Example 5: Parquet sink
try:
    print("Example 5: Saving to Parquet format")
    parquet_sink = ParquetSink('output_data.parquet')
    parquet_sink.save(data)
    print("Data saved to Parquet file output_data.parquet\n")
except ImportError:
    print("Parquet example skipped: pyarrow or fastparquet not installed\n")

# Example 6: Using MultiSink to save to multiple formats at once
print("Example 6: Using MultiSink to save to multiple formats")
multi_sink = MultiSink([
    CSVSink('multi_output.csv'),
    JSONSink('multi_output.json'),
    SQLSink('multi_output.db', 'multi_table')
])
multi_sink.save(data)
print("Data saved to multiple formats using MultiSink\n")

print("All examples completed. Output files created in the current directory.")