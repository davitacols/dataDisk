Customer Data Analysis Example
==============================

This example demonstrates how to use dataDisk for analyzing and transforming customer data in an e-commerce platform.

Code Example
-----------------

.. code-block:: python

    # Import necessary classes from dataDisk
    from dataDisk import DataPipeline, Transformation, Validator

    # Define custom transformations for customer data analysis
    def double_purchase_amount(data):
        data['purchase_amount'] *= 2
        return data

    def categorize_high_value_purchases(data):
        if data['purchase_amount'] > 100:
            data['product_category'] = 'High Value'
        return data

    # Create a data pipeline for customer data analysis
    customer_data_pipeline = DataPipeline()
    customer_data_pipeline.add_task(Transformation(double_purchase_amount))
    customer_data_pipeline.add_task(Transformation(categorize_high_value_purchases))
    customer_data_pipeline.add_task(Validator(lambda data: data['purchase_amount'] > 0))

    # Sample customer data
    customer_data = {
        'customer_id': 1,
        'purchase_amount': 75,
        'purchase_date': '2022-01-15',
        'product_category': 'Electronics'
    }

    try:
        # Process customer data through the pipeline
        processed_customer_data = customer_data_pipeline.process(customer_data)
        print("Processed Customer Data:", processed_customer_data)
    except ValueError as e:
        print(f"Error: {e}")

