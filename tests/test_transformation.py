import unittest
import numpy as np
from dataDisk.transformation import Transformation


class TestTransformation(unittest.TestCase):
    def setUp(self):
        # Sample data with some NaN values
        self.data = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]])

    def test_standardize(self):
        # Test standardization transformation
        transform = Transformation(Transformation.standardize)
        transformed_data = transform.execute(self.data)
        # Check if shape remains the same
        self.assertEqual(self.data.shape, transformed_data.shape)
        # Check mean and std deviation
        self.assertTrue(np.allclose(np.mean(transformed_data, axis=0), 0))
        self.assertTrue(np.allclose(np.std(transformed_data, axis=0), 1, atol=1e-4))

    def test_normalize(self):
        # Test normalization transformation
        transform = Transformation(Transformation.normalize)
        transformed_data = transform.execute(self.data)
        # Check if shape remains the same
        self.assertEqual(self.data.shape, transformed_data.shape)
        # Check norm of each row
        norms = np.linalg.norm(transformed_data, axis=1)
        self.assertTrue(np.allclose(norms, 1))

    def test_onehot_encode(self):
        # Test one-hot encoding transformation
        data = np.array([['A', 'X'], ['B', 'Y'], ['C', 'Z']])
        transform = Transformation(Transformation.onehot_encode)
        transformed_data = transform.execute(data)
        # Check if shape after one-hot encoding
        self.assertEqual((data.shape[0], 6), transformed_data.shape)

    def test_impute_missing(self):
        # Test missing value imputation transformation
        transform = Transformation(Transformation.impute_missing)
        transformed_data = transform.execute(self.data)
        # Check if shape remains the same
        self.assertEqual(self.data.shape, transformed_data.shape)
        # Check if missing values are imputed
        self.assertFalse(np.isnan(transformed_data).any())

    def test_log_transform(self):
        # Test log transformation
        data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        transform = Transformation(Transformation.log_transform)
        transformed_data = transform.execute(data)
        # Check if shape remains the same
        self.assertEqual(data.shape, transformed_data.shape)
        # Check if log transformation is applied
        self.assertTrue(np.allclose(transformed_data, np.log1p(data)))

    def test_sqrt_transform(self):
        # Test sqrt transformation
        transform = Transformation(Transformation.sqrt_transform)
        transformed_data = transform.execute(self.data)
        # Check if shape remains the same
        self.assertEqual(self.data.shape, transformed_data.shape)
        # Check if sqrt transformation is applied correctly
        expected_data = np.sqrt(np.nan_to_num(self.data, nan=0.0))
        self.assertTrue(np.allclose(transformed_data, expected_data, atol=1e-8))

    def test_robust_scale(self):
        # Test robust scaling transformation
        transform = Transformation(Transformation.robust_scale)
        transformed_data = transform.execute(self.data)
        # Check if shape remains the same
        self.assertEqual(self.data.shape, transformed_data.shape)


if __name__ == '__main__':
    unittest.main()
