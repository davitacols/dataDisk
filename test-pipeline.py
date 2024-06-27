import logging
from dataDisk.data_sources import CSVDataSource
from dataDisk.pipeline import DataPipeline
from dataDisk.transformation import Transformation
import os
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the URL of the dataset
dataset_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

# Define the path to save the downloaded dataset
file_path = os.path.join(os.getcwd(), 'iris.data')

# Download the dataset
response = requests.get(dataset_url)
if response.status_code == 200:
    with open(file_path, 'w') as file:
        file.write(response.text)
    logging.info("Dataset downloaded and saved successfully.")
else:
    logging.error("Failed to download the dataset.")
    exit()

# Define the source and sink using the downloaded dataset
source = CSVDataSource(file_path, sep=',')
sink_path = os.path.join(os.getcwd(), 'processed_iris_data.csv')
sink = CSVDataSource(sink_path, sep=',')

# Initialize the data pipeline
pipeline = DataPipeline(source=source, sink=sink)

# Add data cleaning transformation
pipeline.add_task(Transformation.data_cleaning)

# Add normalization transformation
pipeline.add_task(Transformation.normalize)

# Add label encoding transformation
pipeline.add_task(Transformation.label_encode)

# Process the data through the pipeline
try:
    processed_data = pipeline.process()
    logging.info("Data processing completed successfully.")
    logging.info(f"Processed data head:\n{processed_data.head()}")
except Exception as e:
    logging.error(f"Error during data processing: {str(e)}")
