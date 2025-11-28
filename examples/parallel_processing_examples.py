"""
Examples demonstrating the use of parallel processing in dataDisk.
"""

import pandas as pd
import numpy as np
import time
from dataDisk import DataPipeline, Transformation, ParallelProcessor


# Example 1: Basic parallel processing
def basic_parallel_example():
    print("\nExample 1: Basic parallel processing")
    
    # Define some transformation functions
    def double(x):
        return x * 2
    
    def square(x):
        return x ** 2
    
    def add_ten(x):
        return x + 10
    
    # Create a pipeline with multiple steps
    pipeline = DataPipeline()
    pipeline.add_step(Transformation(double))
    pipeline.add_step(Transformation(square))
    pipeline.add_step(Transformation(add_ten))
    
    # Process sequentially
    start_time = time.time()
    sequential_result = pipeline.run(5)
    sequential_time = time.time() - start_time
    
    print(f"Sequential processing result: {sequential_result}")
    print(f"Sequential processing time: {sequential_time:.6f} seconds")
    
    # Process in parallel
    processor = ParallelProcessor()
    start_time = time.time()
    parallel_results = processor.process(pipeline, 5)
    parallel_time = time.time() - start_time
    
    print(f"Parallel processing results: {parallel_results}")
    print(f"Parallel processing time: {parallel_time:.6f} seconds")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")


# Example 2: Parallel map for data processing
def parallel_map_example():
    print("\nExample 2: Parallel map for data processing")
    
    # Create sample data
    data = list(range(1, 1001))
    
    # Define a computationally intensive function
    def intensive_computation(x):
        # Simulate a complex calculation
        result = 0
        for i in range(10000):
            result += np.sin(x * i) * np.cos(x * i)
        return result
    
    # Process sequentially
    start_time = time.time()
    sequential_results = [intensive_computation(x) for x in data[:10]]  # Just process first 10 for demo
    sequential_time = time.time() - start_time
    
    print(f"Sequential processing time for 10 items: {sequential_time:.6f} seconds")
    
    # Process in parallel
    processor = ParallelProcessor()
    start_time = time.time()
    parallel_results = processor.map(intensive_computation, data[:10])
    parallel_time = time.time() - start_time
    
    print(f"Parallel processing time for 10 items: {parallel_time:.6f} seconds")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")
    
    # Check that results are the same
    print(f"Results match: {all(abs(s - p) < 1e-10 for s, p in zip(sequential_results, parallel_results))}")


# Example 3: Batch processing with DataFrames
def dataframe_batch_processing():
    print("\nExample 3: Batch processing with DataFrames")
    
    # Create a sample DataFrame
    df = pd.DataFrame({
        'id': range(1000),
        'value': np.random.rand(1000)
    })
    
    # Split into batches
    batch_size = 100
    batches = [df.iloc[i:i+batch_size] for i in range(0, len(df), batch_size)]
    
    print(f"Created {len(batches)} batches of size {batch_size}")
    
    # Define a processing pipeline
    def process_dataframe(batch_df):
        # Simulate some data processing
        result = batch_df.copy()
        result['value_squared'] = result['value'] ** 2
        result['value_log'] = np.log1p(result['value'])
        result['value_exp'] = np.exp(result['value'])
        # Simulate some computation time
        time.sleep(0.1)
        return result
    
    # Process sequentially
    start_time = time.time()
    sequential_results = [process_dataframe(batch) for batch in batches]
    sequential_time = time.time() - start_time
    
    print(f"Sequential processing time: {sequential_time:.6f} seconds")
    
    # Process in parallel
    processor = ParallelProcessor()
    start_time = time.time()
    parallel_results = processor.map(process_dataframe, batches)
    parallel_time = time.time() - start_time
    
    print(f"Parallel processing time: {parallel_time:.6f} seconds")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")
    
    # Combine results
    sequential_combined = pd.concat(sequential_results)
    parallel_combined = pd.concat(parallel_results)
    
    # Verify results
    print(f"Results match: {sequential_combined.equals(parallel_combined)}")


# Example 4: Using threads vs processes
def threads_vs_processes():
    print("\nExample 4: Using threads vs processes")
    
    # Define a CPU-bound function
    def cpu_bound(n):
        return sum(i * i for i in range(n))
    
    # Define an IO-bound function
    def io_bound(n):
        time.sleep(n / 100)  # Simulate IO operation
        return n
    
    # Test data
    data = [1000000] * 10  # 10 items of the same size
    io_data = [10] * 10  # 10 items with 0.1s sleep each
    
    # Process CPU-bound task with processes
    processor_proc = ParallelProcessor(use_threads=False)
    start_time = time.time()
    processor_proc.map(cpu_bound, data)
    proc_time = time.time() - start_time
    
    print(f"CPU-bound task with processes: {proc_time:.6f} seconds")
    
    # Process CPU-bound task with threads
    processor_thread = ParallelProcessor(use_threads=True)
    start_time = time.time()
    processor_thread.map(cpu_bound, data)
    thread_time = time.time() - start_time
    
    print(f"CPU-bound task with threads: {thread_time:.6f} seconds")
    print(f"Processes vs Threads for CPU-bound: {thread_time / proc_time:.2f}x faster with processes")
    
    # Process IO-bound task with processes
    start_time = time.time()
    processor_proc.map(io_bound, io_data)
    proc_io_time = time.time() - start_time
    
    print(f"IO-bound task with processes: {proc_io_time:.6f} seconds")
    
    # Process IO-bound task with threads
    start_time = time.time()
    processor_thread.map(io_bound, io_data)
    thread_io_time = time.time() - start_time
    
    print(f"IO-bound task with threads: {thread_io_time:.6f} seconds")
    print(f"Processes vs Threads for IO-bound: {proc_io_time / thread_io_time:.2f}x faster with threads")


if __name__ == "__main__":
    print("Running parallel processing examples...")
    basic_parallel_example()
    parallel_map_example()
    dataframe_batch_processing()
    threads_vs_processes()
    print("\nAll examples completed.")