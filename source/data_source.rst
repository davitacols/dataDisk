.. _dataDisk-datasource:

Data Sources and Pipelines Overview
====================================

Introduction
------------

The `dataDisk` package simplifies the creation and execution of data processing pipelines in Python. This documentation section provides an overview of the data source functionality, particularly focusing on the `DataSource`, `CSVDataSource`, and `SQLDataSource` classes.

Data Processing Pipelines
--------------------------

`dataDisk` enables users to define sequential data processing tasks through pipelines. Key components include:

- **DataPipeline**: The core component that allows users to define a sequence of data processing tasks, such as transformations and validations.

- **Transformation**: Represents a task in the pipeline that applies a custom transformation to the input data.

- **Validator**: Checks the validity of the data based on custom conditions.

- **ParallelProcessor**: Enhances performance by allowing the execution of pipeline tasks in parallel.

Data Sources
------------

Data sources play a crucial role in the `dataDisk` framework. The `DataSource` class serves as a base class for different data sources, providing a common interface for reading and writing data.

**CSVDataSource**: Reads and writes data from/to CSV files.

**SQLDataSource**: Reads and writes data from/to SQL databases.

Usage Examples
---------------

Below are examples demonstrating how to use the data sources within the `dataDisk` framework.

CSVDataSource Example
~~~~~~~~~~~~~~~~~~~~~

```python
from dataDisk.data_sources import CSVDataSource

# Create a CSVDataSource instance
csv_source = CSVDataSource('data.csv')

# Read data from CSV
data_read = csv_source.read()

# Write data to CSV
csv_source.write(data_read)
