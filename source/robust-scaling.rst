Robust Scaling
==============

Robust scaling is a method used to scale numerical features in a dataset by removing the median and scaling data based on the interquartile range (IQR). Unlike standard scaling, which uses the mean and standard deviation, robust scaling is less sensitive to outliers and is therefore suitable for datasets with outliers or non-normal distributions.

Purpose
-------

The purpose of robust scaling is to standardize numerical features in a dataset while minimizing the impact of outliers. By removing the median and scaling based on the IQR, robust scaling ensures that the scaling process is less influenced by extreme values.

Usage
-----

To use robust scaling, apply the RobustScaler from the scikit-learn library to your dataset. This scaler will center and scale the data using the median and IQR.

Example
-------

.. code-block:: python

    from sklearn.preprocessing import RobustScaler
    import numpy as np

    # Sample data with some NaN values
    data = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]])

    # Apply robust scaling
    scaler = RobustScaler()
    scaled_data = scaler.fit_transform(data)

Considerations
--------------

- Robust scaling is suitable for datasets with outliers or non-normal distributions.
- It preserves the shape of the original distribution while reducing the impact of outliers.
- Ensure that missing or NaN values are appropriately handled before applying robust scaling.
