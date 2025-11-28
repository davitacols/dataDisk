"""
Examples demonstrating the use of data pipelines in dataDisk.
"""

import pandas as pd
import numpy as np
import logging
from dataDisk.pipeline import DataPipeline, PipelineStep
from dataDisk.data_sources import CSVDataSource, JSONDataSource
from dataDisk.data_sinks import CSVSink, JSONSink
from dataDisk.transformation import Transformation


# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')


# Example 1: Basic pipeline with source and sink
def basic_pipeline_example():
    print("\nExample 1: Basic pipeline with source and sink")
    
    # Create sample data
    data = pd.DataFrame({
        'id': range(1, 6),
        'value': [10, 20, 30, 40, 50],
        'category': ['A', 'B', 'A', 'C', 'B']
    })
    
    # Save to CSV for the example
    data.to_csv('example_input.csv', index=False)
    
    # Create pipeline components
    source = CSVDataSource('example_input.csv')
    sink = CSVSink('example_output.csv')
    
    # Create pipeline
    pipeline = DataPipeline(source=source, sink=sink)
    
    # Define transformations
    def double_values(df):
        df = df.copy()
        df['value'] = df['value'] * 2
        return df
    
    def add_derived_column(df):
        df = df.copy()
        df['value_squared'] = df['value'] ** 2
        return df
    
    def encode_categories(df):
        df = df.copy()
        category_mapping = {'A': 1, 'B': 2, 'C': 3}
        df['category_code'] = df['category'].map(category_mapping)
        return df
    
    # Add steps to pipeline
    pipeline.add_step(double_values)
    pipeline.add_step(add_derived_column)
    pipeline.add_step(encode_categories)
    
    # Process data
    result = pipeline.process()
    
    # Show results
    print("Processed data:")
    print(result)
    
    # Show metrics
    metrics = pipeline.get_metrics()
    print("\nPipeline metrics:")
    print(f"- Load time: {metrics['load_time']:.4f}s")
    print(f"- Processing time: {metrics['total_processing_time']:.4f}s")
    print(f"- Save time: {metrics['save_time']:.4f}s")
    
    for step_name, step_time in metrics['steps'].items():
        print(f"- Step '{step_name}': {step_time:.4f}s")


# Example 2: Custom pipeline steps
def custom_pipeline_steps_example():
    print("\nExample 2: Custom pipeline steps")
    
    # Create sample data
    data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 70000, 80000, 90000]
    })
    
    # Define custom pipeline steps
    class NormalizeStep(PipelineStep):
        def __init__(self, columns):
            self.columns = columns
            
        def execute(self, df):
            df = df.copy()
            for col in self.columns:
                df[col] = (df[col] - df[col].mean()) / df[col].std()
            return df
        
        def get_name(self):
            return f"Normalize({','.join(self.columns)})"
    
    class AddFeatureStep(PipelineStep):
        def __init__(self, name, formula):
            self.name = name
            self.formula = formula
            
        def execute(self, df):
            df = df.copy()
            df[self.name] = self.formula(df)
            return df
        
        def get_name(self):
            return f"AddFeature({self.name})"
    
    # Create pipeline
    pipeline = DataPipeline()
    
    # Add custom steps
    pipeline.add_step(NormalizeStep(['age', 'salary']))
    pipeline.add_step(AddFeatureStep('salary_per_age', lambda df: df['salary'] / df['age']))
    pipeline.add_step(AddFeatureStep('is_high_earner', lambda df: df['salary'] > 0))
    
    # Process data
    result = pipeline.run(data)
    
    # Show results
    print("Processed data:")
    print(result)
    
    # Show metrics
    metrics = pipeline.get_metrics()
    print("\nPipeline metrics:")
    for step_name, step_time in metrics['steps'].items():
        print(f"- Step '{step_name}': {step_time:.4f}s")


# Example 3: Error handling in pipelines
def error_handling_example():
    print("\nExample 3: Error handling in pipelines")
    
    # Create sample data with potential issues
    data = pd.DataFrame({
        'id': range(1, 6),
        'value': [10, 20, None, 40, 50],  # Note the None value
        'text': ['apple', 'banana', 'cherry', 'date', 'elderberry']
    })
    
    # Define steps with potential errors
    def divide_by_ten(df):
        df = df.copy()
        df['value'] = df['value'] / 10  # Will cause error with None
        return df
    
    def text_length(df):
        df = df.copy()
        df['text_length'] = df['text'].str.len()
        return df
    
    # Define error handler
    def handle_error(exception, step_name, data):
        print(f"Error in step '{step_name}': {str(exception)}")
        
        # Fix the issue based on the step
        if step_name == "<lambda>":  # divide_by_ten
            data = data.copy()
            data['value'] = data['value'].fillna(0) / 10
            print("Fixed by filling NA values with 0")
        
        return data
    
    # Create pipeline with error handler
    pipeline = DataPipeline()
    pipeline.set_error_handler(handle_error)
    
    # Add steps
    pipeline.add_step(divide_by_ten)
    pipeline.add_step(text_length)
    
    # Process data
    result = pipeline.run(data)
    
    # Show results
    print("\nProcessed data after error handling:")
    print(result)


# Example 4: Method chaining and pipeline reuse
def method_chaining_example():
    print("\nExample 4: Method chaining and pipeline reuse")
    
    # Create sample datasets
    data1 = pd.DataFrame({
        'id': range(1, 6),
        'value': [10, 20, 30, 40, 50]
    })
    
    data2 = pd.DataFrame({
        'id': range(6, 11),
        'value': [15, 25, 35, 45, 55]
    })
    
    # Create reusable pipeline with method chaining
    pipeline = (DataPipeline()
                .add_step(lambda df: df.assign(value_doubled=df['value'] * 2))
                .add_step(lambda df: df.assign(value_squared=df['value'] ** 2))
                .add_step(lambda df: df.assign(is_high=df['value'] > 30)))
    
    # Process first dataset
    print("Processing first dataset:")
    result1 = pipeline.run(data1)
    print(result1)
    
    # Reset pipeline and process second dataset
    print("\nProcessing second dataset:")
    pipeline.reset()
    result2 = pipeline.run(data2)
    print(result2)
    
    # Compare metrics
    metrics1 = pipeline.get_metrics()
    pipeline.reset()
    result2 = pipeline.run(data2)
    metrics2 = pipeline.get_metrics()
    
    print("\nProcessing time comparison:")
    print(f"- Dataset 1: {metrics1['total_processing_time']:.6f}s")
    print(f"- Dataset 2: {metrics2['total_processing_time']:.6f}s")


if __name__ == "__main__":
    basic_pipeline_example()
    custom_pipeline_steps_example()
    error_handling_example()
    method_chaining_example()
    
    print("\nAll examples completed.")
    
    # Clean up example files
    import os
    for file in ['example_input.csv', 'example_output.csv']:
        if os.path.exists(file):
            os.remove(file)