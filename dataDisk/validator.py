# dataDisk/validator.py

import logging
from pandas import isna
from scipy.stats import skew, kurtosis


class Validator:

    def __init__(self, validate_func):
        self.validate_func = validate_func

    def execute(self, data):
        try:
            if self.validate_func(data):
                return data
            else:
                raise ValueError("Data validation failed.")
        except Exception as e:
            logging.error(f"Error during validation: {str(e)}")
            raise

    @staticmethod
    def check_null(data):
        """Check for null values"""
        return not isna(data).any()

    @staticmethod
    def check_normal_dist(data):
        """Check if data follows normal distribution"""
        s = skew(data)
        k = kurtosis(data)
        return (s < 1) and (k > 2)

    @staticmethod
    def check_range(data, min_val, max_val):
        """Check if data is within given min-max range"""
        return (data >= min_val).all() and (data <= max_val).all()
