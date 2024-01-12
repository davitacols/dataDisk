Usage
=====

Getting Started
---------------

Before using `dataDisk`, make sure you have it installed. You can install it using `pip`:

.. code-block:: shell

    pip install dataDisk

Creating a DataPipeline
-----------------------

To get started with `dataDisk`, you'll typically create a `DataPipeline` to define a sequence of data processing tasks. Each task can be a transformation or a validation.

Example:

.. code-block:: python

    from dataDisk import DataPipeline, Transformation, Validator

    # Define custom transformation functions
    def double(x):
        return x * 2

    def square(x):
        return x ** 2

    # Define custom validation function
    def is_even(x):
        return x if x % 2 == 0 else None

    # Create a DataPipeline
    pipeline = DataPipeline()
    pipeline.add_task(Transformation(double))
    pipeline.add_task(Transformation(square))
    pipeline.add_task(Validator(is_even))

    # Process data through the pipeline
    data = [1, 2, 3, 4, 5]
    result = pipeline.process(data)
    print(result)


Real-world Data Scenario
------------------------

Let's consider a real-world data scenario where you might use the `dataDisk` package. Imagine you are working with a dataset containing information about customers in an e-commerce platform. The dataset has fields like `customer_id`, `purchase_amount`, `purchase_date`, and `product_category`. Your goal is to create a data processing pipeline to analyze and transform this data.

Here's a simple example using the `dataDisk` package:

.. code-block:: python

    from dataDisk import DataPipeline, Transformation, Validator

    # Define the transformations
    def double_purchase_amount(data):
        data['purchase_amount'] *= 2
        return data

    def categorize_high_value_purchases(data):
        if data['purchase_amount'] > 100:
            data['product_category'] = 'High Value'
        return data

    # Create a data pipeline
    pipeline = DataPipeline()

    # Add tasks to the pipeline
    transformation1 = Transformation(double_purchase_amount)
    transformation2 = Transformation(categorize_high_value_purchases)
    validator = Validator(lambda data: data['purchase_amount'] > 0)  # Simple validation for positive purchase amounts

    pipeline.add_task(transformation1)
    pipeline.add_task(transformation2)
    pipeline.add_task(validator)

    # Process data through the pipeline
    data = {
        'customer_id': 1,
        'purchase_amount': 75,
        'purchase_date': '2022-01-15',
        'product_category': 'Electronics'
    }

    try:
        result = pipeline.process(data)
        print("Processed Data:", result)
    except ValueError as e:
        print(f"Error: {e}")

In this scenario:

The `double_purchase_amount` transformation doubles the `purchase_amount` for each customer.
The `categorize_high_value_purchases` transformation updates the `product_category` to 'High Value' for purchases over $100.
The validator ensures that the `purchase_amount` is positive.