import unittest
import pandas as pd
import numpy as np
from dataDisk.transformation import Transformation


class TestTransformation(unittest.TestCase):

    def setUp(self):
        # Create sample data for testing
        self.numeric_data = pd.DataFrame({
            'A': [1, 2, np.nan, 4],
            'B': [5.0, np.nan, 7.0, 8.0],
            'C': [9, 10, 11, 12]
        })

        self.categorical_data = pd.DataFrame({
            'Category': ['A', 'B', 'A', 'B'],
            'Value': [1, 2, 3, 4]
        })

    def test_standardize(self):
        transformed_data = Transformation.standardize(self.numeric_data)
        self.assertEqual(transformed_data.shape, self.numeric_data.shape)
        self.assertFalse(np.isnan(transformed_data).any())

    def test_normalize(self):
        transformed_data = Transformation.normalize(self.numeric_data)
        self.assertEqual(transformed_data.shape, self.numeric_data.shape)
        self.assertFalse(np.isnan(transformed_data).any())

    def test_onehot_encode(self):
        transformed_data = Transformation.onehot_encode(self.categorical_data)
        self.assertEqual(transformed_data.shape[1], 3)  # Check number of columns after encoding

    def test_data_cleaning(self):
        cleaned_data = Transformation.data_cleaning(self.numeric_data)
        self.assertEqual(cleaned_data.shape, self.numeric_data.shape)
        self.assertFalse(cleaned_data.isnull().any().any())

    def test_impute_missing(self):
        imputed_data = Transformation.impute_missing(self.numeric_data)
        self.assertEqual(imputed_data.shape, self.numeric_data.shape)
        self.assertFalse(imputed_data.isnull().any().any())

    def test_log_transform(self):
        transformed_data = Transformation.log_transform(self.numeric_data)
        self.assertEqual(transformed_data.shape, self.numeric_data.shape)
        self.assertFalse(np.isnan(transformed_data).any())

    def test_sqrt_transform(self):
        transformed_data = Transformation.sqrt_transform(self.numeric_data)
        self.assertEqual(transformed_data.shape, self.numeric_data.shape)
        self.assertFalse(np.isnan(transformed_data).any())

    def test_robust_scale(self):
        transformed_data = Transformation.robust_scale(self.numeric_data)
        self.assertEqual(transformed_data.shape, self.numeric_data.shape)
        self.assertFalse(np.isnan(transformed_data).any())

    def test_binning(self):
        transformed_data = Transformation.binning(self.numeric_data['A'])
        self.assertEqual(transformed_data.shape, self.numeric_data['A'].shape)

    def test_interaction_terms(self):
        transformed_data = Transformation.interaction_terms(self.numeric_data)
        self.assertTrue(transformed_data.shape[1] > self.numeric_data.shape[1])

    def test_polynomial_features(self):
        transformed_data = Transformation.polynomial_features(self.numeric_data)
        self.assertTrue(transformed_data.shape[1] > self.numeric_data.shape[1])


if __name__ == '__main__':
    unittest.main()
