# dataDisk/parallel_processor.py
from concurrent.futures import ProcessPoolExecutor
import logging


class ParallelProcessor:
    def __init__(self):
        self.executor = ProcessPoolExecutor()

    def process(self, pipeline, input_data):
        with self.executor as executor:
            # Using list comprehension to gather results from executor.submit
            results = [
                executor.submit(task.execute, input_data)
                for task in pipeline.tasks
            ]

        # Gathering results from the completed tasks
        processed_data = []
        for result in results:
            try:
                processed_data.append(result.result())
            except Exception as e:
                # Log the exception and append
                # an error message to processed_data
                logging.error(f"Error during processing: {str(e)}")
                processed_data.append(f"Error: {e}")

        return processed_data
