Usage
=====

Introduction
------------

`dataDisk` is a Python package designed to simplify the creation and execution of data processing pipelines. It provides a flexible framework for defining sequential tasks, applying transformations, and validating data. Additionally, it includes a `ParallelProcessor` for efficient parallel execution.

Creating a Simple Data Pipeline
-------------------------------

To get started with `dataDisk`, you can create a simple data processing pipeline. First, import the necessary classes:

.. code-block:: python

   from dataDisk.pipeline import DataPipeline
   from dataDisk.tasks import Task

Now, let's create a simple task and a data pipeline:

.. code-block:: python

   # Create a task
   def simple_task(data):
       # Perform some processing on the data
       processed_data = data.upper()
       return processed_data

   task = Task(name="SimpleTask", execute=simple_task)

   # Create a data pipeline
   pipeline = DataPipeline()

   # Add the task to the pipeline
   pipeline.add_task(task)

Executing the Pipeline
----------------------

Once the pipeline is set up, you can execute it by providing input data:

.. code-block:: python

   input_data = "hello, world!"
   result = pipeline.process(input_data)

   print("Result:", result)

This will execute the `simple_task` on the input data and print the result.

Feel free to explore additional features and functionalities offered by `dataDisk` to suit your specific data processing needs.
