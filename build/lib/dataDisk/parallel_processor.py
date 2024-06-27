from concurrent.futures import ProcessPoolExecutor
import logging

class ParallelProcessor:
    def __init__(self):
        self.executor = ProcessPoolExecutor()

    def process(self, pipeline, input_data):
        with self.executor as executor:
            results = [executor.submit(task.execute, input_data) for task in pipeline.tasks]

        processed_data = []
        for result in results:
            try:
                processed_data.append(result.result())
            except Exception as e:
                logging.error(f"Error during processing: {str(e)}")
                processed_data.append(f"Error: {e}")

        return processed_data
