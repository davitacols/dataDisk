from .data_sources import DataSource
from .data_sinks import DataSink
from .transformation import Transformation
import logging


class DataPipeline:
    def __init__(self, source: DataSource, sink: DataSink):
        self.source = source
        self.sink = sink
        self.tasks = []
        self.data = None

    def add_task(self, task):
        if callable(task):
            self.tasks.append(task)
        else:
            raise ValueError("Task must be a callable function")

    def process(self):
        try:
            # Load data from source
            self.data = self.source.load()
            logging.info("Data loaded successfully")

            # Apply each task in the pipeline
            for task in self.tasks:
                if isinstance(task, Transformation):
                    self.data = task.execute(self.data)
                else:
                    self.data = task(self.data)  # For other callable tasks

            # Save processed data to sink
            self.sink.save(self.data)
            logging.info("Data saved successfully")

            return self.data
        except Exception as e:
            logging.error(f"Error during pipeline execution: {str(e)}")
            raise e

# Example usage:
if __name__ == '__main__':
    from dataDisk.data_sources import CSVDataSource
    from dataDisk.data_sinks import CSVSink
    from dataDisk.transformation import Transformation
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Define source and sink
    csv_data_source = CSVDataSource('customer_churn.csv')
    csv_data_sink = CSVSink('processed_customer_churn.csv')
    
    # Create the pipeline
    pipeline = DataPipeline(source=csv_data_source, sink=csv_data_sink)
    
    # Add tasks
    pipeline.add_task(Transformation.data_cleaning)
    pipeline.add_task(Transformation.normalize)
    pipeline.add_task(Transformation.label_encode)
    
    # Process the data
    processed_data = pipeline.process()
    print("Data processing complete.")
