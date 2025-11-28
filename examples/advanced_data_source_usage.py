"""
Advanced examples of data source usage in dataDisk.
"""

import pandas as pd
import numpy as np
import os
import sqlite3
from dataDisk.data_sources import (
    CSVDataSource, SQLDataSource, JSONDataSource, ExcelDataSource
)
from dataDisk.pipeline import DataPipeline
from dataDisk.transformation import Transformation


# Example 1: Working with multiple data sources
def multiple_sources_example():
    print("\nExample 1: Working with multiple data sources")
    
    # Create sample data
    customers = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 
                 'david@example.com', 'eve@example.com']
    })
    
    orders = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003', 'O004', 'O005', 'O006'],
        'customer_id': ['C001', 'C002', 'C001', 'C003', 'C005', 'C002'],
        'amount': [100.50, 200.75, 50.25, 300.00, 150.50, 75.25],
        'date': pd.date_range(start='2023-01-01', periods=6)
    })
    
    # Save to different sources
    customer_source = CSVDataSource('customers.csv')
    customer_source.save(customers)
    
    order_source = JSONDataSource('orders.json')
    order_source.save(orders)
    
    # Load and join data
    loaded_customers = customer_source.load()
    loaded_orders = order_source.load()
    
    # Perform a join operation
    merged_data = pd.merge(
        loaded_orders, 
        loaded_customers, 
        on='customer_id', 
        how='left'
    )
    
    print("Merged customer and order data:")
    print(merged_data.head())
    
    # Calculate order statistics by customer
    customer_stats = merged_data.groupby('customer_id').agg(
        order_count=('order_id', 'count'),
        total_spent=('amount', 'sum'),
        avg_order=('amount', 'mean')
    ).reset_index()
    
    print("\nCustomer order statistics:")
    print(customer_stats)
    
    # Save results to Excel with multiple sheets
    excel_source = ExcelDataSource('customer_analysis.xlsx', sheet_name='merged_data')
    excel_source.save(merged_data)
    
    stats_source = ExcelDataSource('customer_analysis.xlsx', sheet_name='statistics', mode='a')
    stats_source.save(customer_stats)
    
    print("\nResults saved to Excel file with multiple sheets")


# Example 2: Using SQL data source with custom queries
def sql_queries_example():
    print("\nExample 2: Using SQL data source with custom queries")
    
    # Create sample data
    products = pd.DataFrame({
        'product_id': range(1, 11),
        'name': [f'Product {i}' for i in range(1, 11)],
        'category': ['Electronics', 'Clothing', 'Electronics', 'Home', 'Clothing',
                    'Electronics', 'Home', 'Clothing', 'Electronics', 'Home'],
        'price': np.random.uniform(10, 1000, 10).round(2),
        'stock': np.random.randint(0, 100, 10)
    })
    
    # Save to SQLite database
    db_file = 'inventory.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        
    sql_source = SQLDataSource(db_file, 'products')
    sql_source.save(products)
    print(f"Saved {len(products)} products to SQLite database")
    
    # Execute different queries
    queries = {
        'electronics': "SELECT * FROM products WHERE category = 'Electronics'",
        'low_stock': "SELECT * FROM products WHERE stock < 20",
        'expensive': "SELECT * FROM products WHERE price > 500",
        'categories': "SELECT category, COUNT(*) as count, AVG(price) as avg_price FROM products GROUP BY category"
    }
    
    # Execute each query and print results
    for name, query in queries.items():
        result = sql_source.load(query)
        print(f"\n{name.title()} query results:")
        print(result)


# Example 3: Incremental data loading and processing
def incremental_loading_example():
    print("\nExample 3: Incremental data loading and processing")
    
    # Create a database with initial data
    db_file = 'transactions.db'
    if os.path.exists(db_file):
        os.remove(db_file)
    
    # Create initial data
    initial_data = pd.DataFrame({
        'transaction_id': range(1, 101),
        'date': pd.date_range(start='2023-01-01', periods=100),
        'amount': np.random.uniform(10, 1000, 100).round(2),
        'processed': False
    })
    
    # Save initial data
    sql_source = SQLDataSource(db_file, 'transactions')
    sql_source.save(initial_data)
    print(f"Saved {len(initial_data)} initial transactions")
    
    # Function to process unprocessed transactions
    def process_transactions():
        # Get unprocessed transactions
        query = "SELECT * FROM transactions WHERE processed = 0"
        unprocessed = sql_source.load(query)
        
        if len(unprocessed) == 0:
            print("No unprocessed transactions found")
            return
            
        print(f"Found {len(unprocessed)} unprocessed transactions")
        
        # Process the transactions (in this example, just mark as processed)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        for idx in unprocessed['transaction_id']:
            cursor.execute(
                "UPDATE transactions SET processed = 1 WHERE transaction_id = ?", 
                (idx,)
            )
            
        conn.commit()
        conn.close()
        
        print(f"Processed {len(unprocessed)} transactions")
        
        # Verify all are processed
        all_query = "SELECT COUNT(*) as count FROM transactions WHERE processed = 0"
        result = sql_source.load(all_query)
        print(f"Remaining unprocessed transactions: {result['count'].iloc[0]}")
    
    # Run the processing
    process_transactions()
    
    # Add new transactions
    new_data = pd.DataFrame({
        'transaction_id': range(101, 151),
        'date': pd.date_range(start='2023-04-10', periods=50),
        'amount': np.random.uniform(10, 1000, 50).round(2),
        'processed': False
    })
    
    # Append to the database
    conn = sqlite3.connect(db_file)
    new_data.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()
    print(f"Added {len(new_data)} new transactions")
    
    # Process again
    process_transactions()


if __name__ == "__main__":
    multiple_sources_example()
    sql_queries_example()
    incremental_loading_example()
    
    print("\nAll advanced examples completed.")