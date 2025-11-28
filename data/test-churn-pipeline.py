import logging
from dataDisk.pipeline import DataPipeline
from dataDisk.data_sources import CSVDataSource
from dataDisk.transformation import Transformation
from dataDisk.data_sinks import CSVSink

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
pipeline.process()

print("Data processing complete.")
