import pytest
import pandas as pd
import numpy as np
from dataDisk import DataPipeline, Transformation, Validator, ParallelProcessor


# Simple test functions
def double(x):
    return x * 2


def square(x):
    return x ** 2


def is_even(x):
    return x if x % 2 == 0 else None


def add_one(x):
    return x + 1


# Test basic parallel processing
def test_parallel_processing_multiple_tasks():
    pipeline = DataPipeline()
    transformation1 = Transformation(double)
    transformation2 = Transformation(square)
    validator = Transformation(is_even)
    
    pipeline.add_step(transformation1)
    pipeline.add_step(transformation2)
    pipeline.add_step(validator)
    
    processor = ParallelProcessor()
    result = processor.process(pipeline, 3)
    
    assert result[0] == 6  # double(3) = 6
    assert result[1] == 9  # square(3) = 9
    assert isinstance(result[2], str) and "Error" in result[2]  # is_even(3) fails


# Test parallel processing with threads
def test_parallel_processing_with_threads():
    pipeline = DataPipeline()
    transformation1 = Transformation(double)
    transformation2 = Transformation(square)
    
    pipeline.add_step(transformation1)
    pipeline.add_step(transformation2)
    
    processor = ParallelProcessor(use_threads=True)
    result = processor.process(pipeline, 4)
    
    assert result[0] == 8  # double(4) = 8
    assert result[1] == 16  # square(4) = 16


# Test map function
def test_parallel_map():
    processor = ParallelProcessor()
    items = [1, 2, 3, 4, 5]
    
    results = processor.map(double, items)
    
    assert results == [2, 4, 6, 8, 10]


# Test map function with kwargs
def test_parallel_map_with_kwargs():
    def multiply(x, factor=1):
        return x * factor
    
    processor = ParallelProcessor()
    items = [1, 2, 3, 4, 5]
    
    results = processor.map(multiply, items, factor=3)
    
    assert results == [3, 6, 9, 12, 15]


# Test batch processing
def test_batch_processing():
    pipeline = DataPipeline()
    pipeline.add_step(Transformation(double))
    
    processor = ParallelProcessor()
    batch_data = [1, 2, 3, 4, 5]
    
    results = processor.batch_process(pipeline, batch_data)
    
    assert results == [2, 4, 6, 8, 10]


# Test with pandas DataFrame
def test_parallel_processing_with_dataframe():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    })
    
    def process_row(row):
        return row['A'] * row['B']
    
    processor = ParallelProcessor()
    results = processor.map(process_row, [row for _, row in df.iterrows()])
    
    assert results == [10, 40, 90, 160, 250]


# Test error handling
def test_error_handling():
    def problematic_function(x):
        if x == 3:
            raise ValueError("Value cannot be 3")
        return x * 2
    
    processor = ParallelProcessor()
    items = [1, 2, 3, 4, 5]
    
    results = processor.map(problematic_function, items)
    
    assert results[0] == 2
    assert results[1] == 4
    assert results[2] is None  # Error case
    assert results[3] == 8
    assert results[4] == 10


# Test with custom max_workers
def test_custom_max_workers():
    processor = ParallelProcessor(max_workers=2)
    items = [1, 2, 3, 4, 5]
    
    results = processor.map(double, items)
    
    assert results == [2, 4, 6, 8, 10]