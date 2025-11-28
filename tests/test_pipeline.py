import pytest
import pandas as pd
import os
import tempfile
from dataDisk.pipeline import DataPipeline, PipelineStep
from dataDisk.data_sources import CSVDataSource
from dataDisk.data_sinks import CSVSink
from dataDisk.transformation import Transformation


# Create sample data
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [6, 7, 8, 9, 10],
        'category': ['A', 'B', 'A', 'B', 'A'],
        'feature3': [None, 2.0, None, 4.0, 5.0]
    })


# Create temporary files
@pytest.fixture
def temp_files():
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as input_file, \
         tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as output_file:
        input_path = input_file.name
        output_path = output_file.name
    
    yield input_path, output_path
    
    # Clean up
    for path in [input_path, output_path]:
        if os.path.exists(path):
            os.remove(path)


# Custom pipeline step
class CustomStep(PipelineStep):
    def __init__(self, column, multiplier):
        self.column = column
        self.multiplier = multiplier
        
    def execute(self, data):
        data = data.copy()
        data[self.column] = data[self.column] * self.multiplier
        return data
    
    def get_name(self):
        return f"MultiplyBy{self.multiplier}"


# Test basic pipeline functionality
def test_pipeline_process(sample_data, temp_files):
    input_path, output_path = temp_files
    
    # Save sample data to input file
    sample_data.to_csv(input_path, index=False)
    
    # Initialize pipeline components
    source = CSVDataSource(input_path)
    sink = CSVSink(output_path)
    pipeline = DataPipeline(source=source, sink=sink)
    
    # Add steps to the pipeline
    pipeline.add_step(lambda df: df.fillna(df.mean()))
    pipeline.add_step(lambda df: df.drop(columns=['category']))
    
    # Process the data
    processed_data = pipeline.process()
    
    # Check if output file exists
    assert os.path.exists(output_path)
    
    # Load the processed data
    output_data = pd.read_csv(output_path)
    
    # Verify transformations
    assert processed_data.shape[0] == sample_data.shape[0]
    assert 'category' not in output_data.columns
    assert not processed_data['feature3'].isna().any()


# Test method chaining
def test_pipeline_method_chaining(sample_data):
    # Create pipeline with method chaining
    pipeline = DataPipeline()
    
    # Define simple transformations
    def double(df):
        return df * 2
    
    def add_column(df):
        df = df.copy()
        df['new_column'] = 1
        return df
    
    # Chain methods
    result = (pipeline
              .add_step(double)
              .add_step(add_column)
              .run(sample_data))
    
    # Verify transformations
    assert 'new_column' in result.columns
    assert result['feature1'][0] == sample_data['feature1'][0] * 2


# Test custom pipeline step
def test_custom_pipeline_step(sample_data):
    pipeline = DataPipeline()
    
    # Add custom step
    custom_step = CustomStep('feature1', 10)
    pipeline.add_step(custom_step)
    
    # Process data
    result = pipeline.run(sample_data)
    
    # Verify transformation
    assert result['feature1'][0] == sample_data['feature1'][0] * 10
    
    # Check metrics
    metrics = pipeline.get_metrics()
    assert 'MultiplyBy10' in metrics['steps']
    assert metrics['steps']['MultiplyBy10'] > 0


# Test error handling
def test_pipeline_error_handling(sample_data):
    pipeline = DataPipeline()
    
    # Define a step that will raise an error
    def problematic_step(df):
        raise ValueError("Test error")
    
    # Define error handler
    def error_handler(exception, step_name, data):
        return data  # Return original data on error
    
    # Add steps
    pipeline.add_step(lambda df: df * 2)
    pipeline.add_step(problematic_step)
    pipeline.add_step(lambda df: df + 1)  # This should not execute
    
    # Set error handler
    pipeline.set_error_handler(error_handler)
    
    # Process data
    result = pipeline.run(sample_data)
    
    # Verify that error handler worked and returned the data from the previous step
    assert result['feature1'][0] == sample_data['feature1'][0] * 2


# Test pipeline with transformation objects
def test_pipeline_with_transformations(sample_data):
    pipeline = DataPipeline()
    
    # Create transformation
    def double(x):
        return x * 2
    
    transformation = Transformation(double)
    
    # Add transformation to pipeline
    pipeline.add_step(transformation)
    
    # Process data
    result = pipeline.run(sample_data)
    
    # Verify transformation
    assert result['feature1'][0] == sample_data['feature1'][0] * 2


# Test pipeline metrics
def test_pipeline_metrics(sample_data, temp_files):
    input_path, output_path = temp_files
    
    # Save sample data to input file
    sample_data.to_csv(input_path, index=False)
    
    # Initialize pipeline
    source = CSVDataSource(input_path)
    sink = CSVSink(output_path)
    pipeline = DataPipeline(source=source, sink=sink)
    
    # Add steps
    pipeline.add_step(lambda df: df.fillna(0))
    pipeline.add_step(lambda df: df * 2)
    
    # Process data
    pipeline.process()
    
    # Check metrics
    metrics = pipeline.get_metrics()
    assert 'load_time' in metrics
    assert 'save_time' in metrics
    assert 'total_processing_time' in metrics
    assert len(metrics['steps']) == 2


# Test pipeline reset
def test_pipeline_reset(sample_data):
    pipeline = DataPipeline()
    
    # Add step and run
    pipeline.add_step(lambda df: df * 2)
    pipeline.run(sample_data)
    
    # Check that metrics exist
    assert pipeline.get_metrics()
    
    # Reset pipeline
    pipeline.reset()
    
    # Check that metrics are cleared
    assert pipeline.get_metrics() == {}