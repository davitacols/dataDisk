import logging
from pandas import isna, Series
from scipy.stats import shapiro
import re


def check_null(data):
    """
    Checks for null values in the data.

    Parameters:
        data (Series): The data to check for null values.

    Returns:
        bool: True if no null values, False otherwise.
    """
    return not isna(data).any()


def check_normal_dist(data, alpha=0.05):
    """
    Checks if data follows a normal distribution using the Shapiro-Wilk test.

    Parameters:
        data (Series): The data to check for normal distribution.
        alpha (float): The significance level for the Shapiro-Wilk test.

    Returns:
        bool: True if data follows a normal distribution, False otherwise.
    """
    stat, p_value = shapiro(data)
    return p_value > alpha


def check_range(data, min_val, max_val):
    """
    Checks if data is within a given min-max range.

    Parameters:
        data (Series): The data to check.
        min_val (float): The minimum value of the range.
        max_val (float): The maximum value of the range.

    Returns:
        bool: True if data is within the range, False otherwise.
    """
    return (data >= min_val).all() and (data <= max_val).all()


def check_positive(data):
    """
    Checks if all data values are positive.

    Parameters:
        data (Series): The data to check.

    Returns:
        bool: True if all values are positive, False otherwise.
    """
    return (data > 0).all()


def check_unique(data):
    """
    Checks if all data values are unique.

    Parameters:
        data (Series): The data to check.

    Returns:
        bool: True if all values are unique, False otherwise.
    """
    return data.is_unique


def check_monotonic(data, increasing=True):
    """
    Checks if data values are monotonically increasing or decreasing.

    Parameters:
        data (Series): The data to check.
        increasing (bool): Set to True to check for increasing order, False for decreasing order.

    Returns:
        bool: True if data is monotonic according to the 'increasing' parameter, False otherwise.
    """
    if increasing:
        return data.is_monotonic_increasing
    else:
        return data.is_monotonic_decreasing


def check_frequency(data, expected_freq, tolerance=0.05):
    """
    Checks if the frequency of data values matches the expected frequency within a given tolerance.

    Parameters:
        data (Series): The data to check.
        expected_freq (dict): A dictionary with expected frequencies for each value.
        tolerance (float): The tolerance for frequency deviation.

    Returns:
        bool: True if frequencies match within the tolerance, False otherwise.
    """
    actual_freq = data.value_counts(normalize=True).to_dict()
    for value, freq in expected_freq.items():
        if abs(actual_freq.get(value, 0) - freq) > tolerance:
            return False
    return True


def check_categorical(data, categories):
    """
    Checks if all data values belong to a set of specified categories.

    Parameters:
        data (Series): The data to check.
        categories (list): The list of valid categories.

    Returns:
        bool: True if all values belong to the categories, False otherwise.
    """
    return data.isin(categories).all()


def check_string_length(data, min_length=None, max_length=None):
    """
    Checks if the length of string data is within the specified range.

    Parameters:
        data (Series): The data to check.
        min_length (int): The minimum length of the strings.
        max_length (int): The maximum length of the strings.

    Returns:
        bool: True if the length of all strings is within the range, False otherwise.
    """
    if min_length is not None:
        if not (data.str.len() >= min_length).all():
            return False
    if max_length is not None:
        if not (data.str.len() <= max_length).all():
            return False
    return True


def check_pattern(data, pattern):
    """
    Checks if all data values match a given regular expression pattern.

    Parameters:
        data (Series): The data to check.
        pattern (str): The regular expression pattern to match.

    Returns:
        bool: True if all values match the pattern, False otherwise.
    """
    return data.str.match(pattern).all()


class Validator:
    """
    A class to validate data based on user-defined criteria.

    Attributes:
        validate_func (callable): A function that takes a single argument (data) and returns a boolean.
    """

    def __init__(self, validate_func):
        """
        Constructs all the necessary attributes for the Validator object.

        Parameters:
            validate_func (callable): The function to use for validation.
        """
        self.validate_func = validate_func

    def execute(self, data):
        """
        Executes the validation function on the provided data.

        Parameters:
            data (Series): The data to validate.

        Returns:
            Series: The original data if validation passes.

        Raises:
            ValueError: If the data fails validation.
            Exception: If any other exception occurs during validation.
        """
        try:
            if self.validate_func(data):
                return data
            else:
                raise ValueError("Data validation failed.")
        except Exception as e:
            logging.error(f"Error during validation: {e}")
            raise
