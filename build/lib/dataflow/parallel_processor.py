# dataflow/parallel_processor.py
from concurrent.futures import ProcessPoolExecutor


class ParallelProcessor:
    def __init__(self):
        self.executor = ProcessPoolExecutor()

    def process(self, pipeline, input_data):
        # Using list comprehension to gather results from executor.submit
        results = [executor.submit(task.execute, input_data) for task in pipeline.tasks]

        # Gathering results from the completed tasks
        processed_data = [result.result() for result in results]

        return processed_data
