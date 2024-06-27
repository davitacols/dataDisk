import unittest
from pandas import Series
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

from dataDisk.validator import (
    check_null, check_normal_dist, check_range, check_positive,
    check_unique, check_monotonic, check_frequency, check_categorical,
    check_string_length, check_pattern, Validator
)


class TestValidator(unittest.TestCase):
    def test_check_null(self):
        data = Series([1, 2, 3, 4, 5])
        self.assertTrue(check_null(data))
        data = Series([1, 2, np.nan, 4, 5])
        self.assertFalse(check_null(data))

    def test_check_normal_dist(self):
        data = Series(np.array(
            [
                -0.9114, 0.1935, 1.6347, -0.0639, -0.0556, 0.4129, 0.3147, -0.4272, -0.0174, -0.2324
                ]
        ))
        self.assertTrue(check_normal_dist(data))
        data = Series(np.random.exponential(1, 1000))
        self.assertFalse(check_normal_dist(data))

    def test_check_range(self):
        data = Series(range(10))
        self.assertTrue(check_range(data, 0, 9))
        self.assertFalse(check_range(data, 1, 9))
        self.assertFalse(check_range(data, 0, 8))

    def test_check_positive(self):
        data = Series([1, 2, 3, 4, 5])
        self.assertTrue(check_positive(data))
        data = Series([-1, 2, 3, 4, 5])
        self.assertFalse(check_positive(data))

    def test_check_unique(self):
        data = Series([1, 2, 3, 4, 5])
        self.assertTrue(check_unique(data))
        data = Series([1, 2, 3, 4, 2])
        self.assertFalse(check_unique(data))

    def test_check_monotonic(self):
        data = Series(range(10))
        self.assertTrue(check_monotonic(data, increasing=True))
        self.assertFalse(check_monotonic(data, increasing=False))
        data = Series(range(10, 0, -1))
        self.assertTrue(check_monotonic(data, increasing=False))
        self.assertFalse(check_monotonic(data, increasing=True))

    def test_check_frequency(self):
        data = Series([1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
        expected_freq = {1: 0.2, 2: 0.2, 3: 0.3, 4: 0.4}
        self.assertTrue(check_frequency(data, expected_freq))
        expected_freq = {1: 0.3, 2: 0.2, 3: 0.3, 4: 0.4}
        self.assertFalse(check_frequency(data, expected_freq))

    def test_check_categorical(self):
        data = Series(["apple", "banana", "orange", "apple", "banana"])
        categories = ["apple", "banana", "orange"]
        self.assertTrue(check_categorical(data, categories))
        categories = ["apple", "banana"]
        self.assertFalse(check_categorical(data, categories))

    def test_check_string_length(self):
        data = Series(["apple", "banana", "orange"])
        self.assertTrue(check_string_length(data, min_length=3, max_length=6))
        self.assertTrue(check_string_length(data, min_length=5, max_length=6))  # Corrected assertion
        self.assertFalse(check_string_length(data, min_length=3, max_length=5))

    def test_check_pattern(self):
        data = Series(["apple", "banana", "orange"])
        pattern = r"^[a-z]+$"
        self.assertTrue(check_pattern(data, pattern))
        pattern = r"^[A-Z]+$"
        self.assertFalse(check_pattern(data, pattern))

    def test_validator_execute(self):
        data = Series([1, 2, 3, 4, 5])
        validator = Validator(check_positive)
        self.assertEqual(validator.execute(data).tolist(), data.tolist())
        validator = Validator(lambda x: check_range(x, 0, 3))
        with self.assertRaises(ValueError):
            validator.execute(data)

if __name__ == "__main__":
    unittest.main()