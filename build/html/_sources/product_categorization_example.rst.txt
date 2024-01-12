Product Categorization Example
==============================

Explore how to use dataDisk for categorizing products based on specific criteria.

Code Example
-----------------

.. code-block:: python

    # Import necessary classes from dataDisk
    from dataDisk import DataPipeline, Transformation, Validator

    # Define custom transformations for product categorization
    def categorize_products(data):
        if data['purchase_amount'] > 50:
            data['product_category'] = 'High Value'
        else:
            data['product_category'] = 'Regular'
        return data

    # Create a data pipeline for product categorization
    product_categorization_pipeline = DataPipeline()
    product_categorization_pipeline.add_task(Transformation(categorize_products))
    product_categorization_pipeline.add_task(Validator(lambda data: data['purchase_amount'] > 0))

    # Sample product data
    product_data = {
        'product_id': 101,
        'purchase_amount': 60,
        'purchase_date': '2022-01-20'
    }

    try:
        # Process product data through the pipeline
        processed_product_data = product_categorization_pipeline.process(product_data)
        print("Processed Product Data:", processed_product_data)
    except ValueError as e:
        print(f"Error: {e}")

