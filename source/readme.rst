dataDisk
========

dataDisk is a Python package designed to simplify the creation and execution of data processing pipelines. It provides a flexible framework for defining sequential tasks, applying transformations, and validating data. Additionally, it includes a ParallelProcessor for efficient parallel execution.

Key Components
--------------

1. **DataPipeline**
   DataPipeline is the core component that allows users to define a sequence of data processing tasks. These tasks can include transformations and validations. The pipeline follows a sequential order, ensuring that data is processed step by step.

   Example:

   .. code-block:: python

      pipeline = DataPipeline()
      pipeline.add_task(Transformation(double))
      pipeline.add_task(Transformation(square))
      pipeline.add_task(Validator(is_even))

2. **Transformation**

    The `Transformation` class represents a task in the pipeline that applies a custom transformation to the input data. Users can define their transformation functions and easily integrate them into the pipeline.

    Example:
    
    .. code-block:: python

      def double(x):
          return x * 2
      
      transformation = Transformation(double)

3. **Validator**

    The `Validator` class is responsible for checking the validity of the data based on custom conditions. If the data passes the validation, it continues through the pipeline; otherwise, an error is raised.

    Example:

    .. code-block:: python

      def is_even(x):
          return x if x % 2 == 0 else None
      
      validator = Validator(is_even)

Also
~~~~

  Register a custom transformation:

  .. code-block:: python

      Transformation.register_custom_transformation('custom_multiply_by_3', lambda x: x * 3)

  Register a custom validator:

  .. code-block:: python

      Validator.register_custom_validator('custom_is_positive', lambda x: x > 0)

4. **ParallelProcessor**

    `ParallelProcessor` enhances performance by allowing the execution of pipeline tasks in parallel. It utilizes Python's `concurrent.futures` module to efficiently process data concurrently, taking advantage of multi-core systems.

    Example:
    
    .. code-block:: python

      processor = ParallelProcessor()
      result = processor.process(pipeline, [1, 2, 3, 4, 5])

Installation
------------

Install the package using pip:

.. code-block:: bash

    pip install dataDisk

Testing
-------

Run the included test suite to ensure the stability and correctness of the package:

.. code-block:: bash

    python -m unittest discover tests

Contributing
------------

If you'd like to contribute to the development of DataDisk, please follow the guidelines in :ref:`CONTRIBUTING`.

License
-------

This project is licensed under the MIT License - see the :ref:`LICENSE` file for details.
