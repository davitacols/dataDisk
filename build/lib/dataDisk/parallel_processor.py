from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import logging
import multiprocessing
from typing import List, Any, Callable, Dict, Union, Optional


class ParallelProcessor:
    """
    Process pipeline tasks in parallel using multiprocessing or multithreading.
    """
    
    def __init__(self, max_workers: Optional[int] = None, use_threads: bool = False, 
                 timeout: Optional[float] = None):
        """
        Initialize the parallel processor.
        
        Args:
            max_workers: Maximum number of workers to use. Default is CPU count.
            use_threads: If True, use ThreadPoolExecutor instead of ProcessPoolExecutor.
            timeout: Maximum time in seconds to wait for task completion.
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.use_threads = use_threads
        self.timeout = timeout
        self._executor_class = ThreadPoolExecutor if use_threads else ProcessPoolExecutor
        
    def process(self, pipeline, input_data: Any) -> List[Any]:
        """
        Process pipeline tasks in parallel.
        
        Args:
            pipeline: Pipeline containing tasks to execute
            input_data: Input data to process
            
        Returns:
            List of results from each task
        """
        with self._executor_class(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(task.execute, input_data): i 
                for i, task in enumerate(pipeline.tasks)
            }
            
            # Initialize results list with placeholders
            results = [None] * len(pipeline.tasks)
            
            # Process completed futures as they complete
            for future in as_completed(futures, timeout=self.timeout):
                task_index = futures[future]
                try:
                    results[task_index] = future.result()
                except Exception as e:
                    logging.error(f"Error in task {task_index}: {str(e)}")
                    results[task_index] = f"Error: {e}"
                    
        return results
    
    def map(self, func: Callable, items: List[Any], **kwargs) -> List[Any]:
        """
        Apply a function to each item in a list in parallel.
        
        Args:
            func: Function to apply
            items: List of items to process
            **kwargs: Additional arguments to pass to the function
            
        Returns:
            List of results
        """
        results = []
        
        with self._executor_class(max_workers=self.max_workers) as executor:
            if kwargs:
                futures = [executor.submit(func, item, **kwargs) for item in items]
            else:
                futures = [executor.submit(func, item) for item in items]
                
            for future in as_completed(futures, timeout=self.timeout):
                try:
                    results.append(future.result())
                except Exception as e:
                    logging.error(f"Error during parallel map: {str(e)}")
                    results.append(None)
                    
        return results
    
    def batch_process(self, pipeline, batch_data: List[Any]) -> List[List[Any]]:
        """
        Process multiple input items through the same pipeline in parallel.
        
        Args:
            pipeline: Pipeline to execute
            batch_data: List of input data items
            
        Returns:
            List of results for each input item
        """
        with self._executor_class(max_workers=self.max_workers) as executor:
            futures = [executor.submit(pipeline.run, item) for item in batch_data]
            
            results = []
            for future in as_completed(futures, timeout=self.timeout):
                try:
                    results.append(future.result())
                except Exception as e:
                    logging.error(f"Error during batch processing: {str(e)}")
                    results.append(f"Error: {e}")
                    
        return results
