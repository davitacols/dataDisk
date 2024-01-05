Example
=======

In this example, we'll create a more complex data processing pipeline using `dataDisk`. The pipeline will consist of multiple tasks to illustrate how to organize and sequence different processing steps.

```python
# Import necessary classes
from dataDisk.pipeline import DataPipeline
from dataDisk.tasks import Task

# Define tasks
def load_data_task(data):
    # Simulate loading data from a source
    loaded_data = f"Loaded data: {data}"
    return loaded_data

def preprocess_data_task(data):
    # Simulate data preprocessing
    preprocessed_data = data.upper()
    return preprocessed_data

def analyze_data_task(data):
    # Simulate data analysis
    analyzed_data = f"Analysis result: {data}"
    return analyzed_data

# Create tasks
load_data = Task(name="LoadData", execute=load_data_task)
preprocess_data = Task(name="PreprocessData", execute=preprocess_data_task)
analyze_data = Task(name="AnalyzeData", execute=analyze_data_task)

# Create a data pipeline
pipeline = DataPipeline()

# Add tasks to the pipeline
pipeline.add_task(load_data)
pipeline.add_task(preprocess_data)
pipeline.add_task(analyze_data)

# Execute the pipeline
input_data = "raw data"
result = pipeline.process(input_data)

# Print the result
print("Final Result:", result)
