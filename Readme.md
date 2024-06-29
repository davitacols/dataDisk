# dataDisk

`dataDisk` is a Python package designed to simplify the creation and execution of data processing pipelines. It provides a flexible framework for defining sequential tasks, applying transformations, and validating data. Additionally, it includes features for efficient parallel execution.

## Key Features

- **DataPipeline**: Define a sequence of data processing tasks in a straightforward manner.
- **Transformation**: Apply custom transformations to your data easily.
- **Validator**: Ensure your data meets specific conditions.
- **ParallelProcessor**: Execute pipeline tasks in parallel for improved performance.
- **Data Sinks**: Save processed data to various formats like CSV, Excel, and SQLite.

## Installation

Install the package using pip:

```bash
pip install dataDisk
```


## Transformations

Transformations allow you to apply various operations to your data. Here's a brief overview of available transformations:

- **Standardize**: Scale features to have zero mean and unit variance.
- **Normalize**: Scale features to have zero mean and unit variance.
- **Label Encode**: Convert categorical labels to numeric values.
- **OneHot Encode**: Convert categorical labels to one-hot encoded vectors.
- **Data Cleaning**: Perform data cleaning operations like filling missing values and encoding categories.

### Example of a custom transformation:

```bash
from dataDisk.transformation import Transformation

def double(x):
    return x * 2

transformation = Transformation(double)
```


## Data Sinks
Data sinks allow you to save processed data to various formats:

- **CSVDataSink**: Save data to a CSV file.
- **ExcelDataSink**: Save data to an Excel file.
- **SQLiteDataSink**: Save data to an SQLite database.

### Example of using a data sink:
```bash
from dataDisk.data_sinks import CSVDataSink

csv_data_sink = CSVDataSink('output.csv')
csv_data_sink.save(data)


