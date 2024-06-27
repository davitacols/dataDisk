from .data_sources import DataSource
import logging


class DataPipeline:
    def __init__(self, source, sink):
        self.source = source
        self.sink = sink
        self.tasks = []

    def add_task(self, task):
        if callable(task):
            self.tasks.append(task)
        else:
            raise ValueError("Task must be a callable function")

    def process(self):
        try:
            # Load data from source
            data = self.source.load()
            logging.info("Data loaded successfully")

            # Apply each task in the pipeline
            for task in self.tasks:
                data = task(data)
            
            # Save processed data to sink
            self.sink.save(data)
            logging.info("Data saved successfully")

            return data
        except Exception as e:
            logging.error(f"Error during pipeline execution: {str(e)}")
            raise e
