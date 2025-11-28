"""
Advanced examples of data sink usage in dataDisk.
"""

import pandas as pd
import numpy as np
import os
from dataDisk.data_sinks import (
    CSVSink, JSONSink, SQLSink, ExcelSink, ParquetSink, MultiSink
)
from dataDisk.pipeline import DataPipeline
from dataDisk.transformation import Transformation


# Create a more complex dataset
def create_sample_data(rows=1000):
    np.random.seed(42)
    
    # Generate dates for the last 1000 days
    dates = pd.date_range(end=pd.Timestamp.now(), periods=rows)
    
    # Create customer IDs and products
    customer_ids = [f"CUST-{i:04d}" for i in np.random.randint(1, 500, size=rows)]
    products = [f"PROD-{i:03d}" for i in np.random.randint(1, 50, size=rows)]
    
    # Generate transaction data
    data = pd.DataFrame({
        'transaction_date': dates,
        'customer_id': customer_ids,
        'product_id': products,
        'quantity': np.random.randint(1, 10, size=rows),
        'unit_price': np.random.uniform(10, 1000, size=rows).round(2),
        'is_promotion': np.random.choice([True, False], size=rows, p=[0.3, 0.7])
    })
    
    # Calculate total price
    data['total_price'] = data['quantity'] * data['unit_price']
    data.loc[data['is_promotion'], 'total_price'] *= 0.9  # 10% discount for promotions
    
    return data


# Example 1: Partitioned CSV output
def partitioned_csv_example(data):
    print("\nExample 1: Partitioned CSV output by date")
    
    # Create directory for partitioned data
    os.makedirs("partitioned_output", exist_ok=True)
    
    # Group by month and save to separate files
    for name, group in data.groupby(data['transaction_date'].dt.strftime('%Y-%m')):
        file_path = f"partitioned_output/transactions_{name}.csv"
        sink = CSVSink(file_path)
        sink.save(group)
        print(f"Saved {len(group)} records to {file_path}")


# Example 2: Pipeline with multiple sinks
def pipeline_with_sinks_example(data):
    print("\nExample 2: Data pipeline with multiple sinks")
    
    # Define transformations
    def add_derived_columns(df):
        df = df.copy()
        df['transaction_year'] = df['transaction_date'].dt.year
        df['transaction_month'] = df['transaction_date'].dt.month
        df['is_high_value'] = df['total_price'] > 1000
        return df
    
    def aggregate_by_customer(df):
        return df.groupby('customer_id').agg(
            transaction_count=('transaction_date', 'count'),
            total_spent=('total_price', 'sum'),
            avg_order_value=('total_price', 'mean'),
            first_purchase=('transaction_date', 'min'),
            last_purchase=('transaction_date', 'max')
        ).reset_index()
    
    # Create pipeline
    pipeline = DataPipeline()
    pipeline.add_step(Transformation(add_derived_columns))
    
    # Process data
    processed_data = pipeline.run(data)
    
    # Save detailed data
    detail_sink = CSVSink('pipeline_output_detail.csv')
    detail_sink.save(processed_data)
    print(f"Saved detailed data with {len(processed_data)} records")
    
    # Create and save customer summary
    customer_summary = aggregate_by_customer(processed_data)
    summary_sink = MultiSink([
        CSVSink('pipeline_output_summary.csv'),
        ExcelSink('pipeline_output_summary.xlsx'),
        JSONSink('pipeline_output_summary.json', orient='records')
    ])
    summary_sink.save(customer_summary)
    print(f"Saved customer summary with {len(customer_summary)} records to multiple formats")


# Example 3: Incremental database updates
def incremental_db_example(data):
    print("\nExample 3: Incremental database updates")
    
    # Split data into "existing" and "new" data
    existing_data = data.iloc[:800].copy()
    new_data = data.iloc[800:].copy()
    
    # First save the "existing" data
    initial_sink = SQLSink('transactions.db', 'transactions', if_exists='replace')
    initial_sink.save(existing_data)
    print(f"Saved initial {len(existing_data)} records to database")
    
    # Now append the "new" data
    append_sink = SQLSink('transactions.db', 'transactions', if_exists='append')
    append_sink.save(new_data)
    print(f"Appended {len(new_data)} new records to database")
    
    # Verify total count
    import sqlite3
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Total records in database: {total_count}")


if __name__ == "__main__":
    print("Creating sample transaction data...")
    transaction_data = create_sample_data()
    print(f"Created dataset with {len(transaction_data)} records")
    
    # Run examples
    partitioned_csv_example(transaction_data)
    pipeline_with_sinks_example(transaction_data)
    incremental_db_example(transaction_data)
    
    print("\nAll advanced examples completed.")