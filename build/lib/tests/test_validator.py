import pytest
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

from dataDisk.validator import (
    ValidationResult, ValidationError, Validator,
    check_null, check_normal_dist, check_range, check_positive,
    check_unique, check_monotonic, check_frequency, check_categorical,
    check_string_length, check_pattern, check_outliers, check_correlation
)


# Create sample data for testing
@pytest.fixture
def numeric_data():
    return pd.Series([1, 2, 3, 4, 5])


@pytest.fixture
def numeric_data_with_nulls():
    return pd.Series([1, 2, np.nan, 4, 5])


@pytest.fixture
def categorical_data():
    return pd.Series(["apple", "banana", "orange", "apple", "banana"])


@pytest.fixture
def normal_data():
    np.random.seed(42)
    return pd.Series(np.random.normal(0, 1, 100))


@pytest.fixture
def non_normal_data():
    np.random.seed(42)
    return pd.Series(np.random.exponential(1, 100))


# Test ValidationResult class
def test_validation_result():
    # Test successful validation
    result = ValidationResult(True, "Test passed")
    assert result.is_valid
    assert bool(result) is True
    assert "PASSED" in str(result)
    
    # Test failed validation
    result = ValidationResult(False, "Test failed", {"error": "Invalid data"})
    assert not result.is_valid
    assert bool(result) is False
    assert "FAILED" in str(result)
    assert result.details["error"] == "Invalid data"


# Test check_null function
def test_check_null(numeric_data, numeric_data_with_nulls):
    # Test with no nulls
    result = check_null(numeric_data)
    assert result.is_valid
    assert "No null values" in result.message
    
    # Test with nulls
    result = check_null(numeric_data_with_nulls)
    assert not result.is_valid
    assert "Found 1 null values" in result.message
    assert result.details["null_count"] == 1


# Test check_normal_dist function
def test_check_normal_dist(normal_data, non_normal_data):
    # Test with normal data
    result = check_normal_dist(normal_data)
    assert result.is_valid
    assert "normal distribution" in result.message
    assert "p_value" in result.details
    
    # Test with non-normal data
    result = check_normal_dist(non_normal_data)
    assert not result.is_valid
    assert "does not follow normal distribution" in result.message


# Test check_range function
def test_check_range(numeric_data):
    # Test within range
    result = check_range(numeric_data, 1, 5)
    assert result.is_valid
    assert "within range" in result.message
    
    # Test outside range (min)
    result = check_range(numeric_data, 2, 5)
    assert not result.is_valid
    assert "outside range" in result.message
    assert result.details["below_min_count"] == 1
    
    # Test outside range (max)
    result = check_range(numeric_data, 1, 4)
    assert not result.is_valid
    assert "outside range" in result.message
    assert result.details["above_max_count"] == 1


# Test check_positive function
def test_check_positive():
    # Test with positive data
    positive_data = pd.Series([1, 2, 3, 4, 5])
    result = check_positive(positive_data)
    assert result.is_valid
    assert "All values are positive" in result.message
    
    # Test with non-positive data
    non_positive_data = pd.Series([-1, 0, 1, 2, 3])
    result = check_positive(non_positive_data)
    assert not result.is_valid
    assert "non-positive values" in result.message
    assert result.details["negative_count"] == 2


# Test check_unique function
def test_check_unique():
    # Test with unique data
    unique_data = pd.Series([1, 2, 3, 4, 5])
    result = check_unique(unique_data)
    assert result.is_valid
    assert "All values are unique" in result.message
    
    # Test with non-unique data
    non_unique_data = pd.Series([1, 2, 2, 3, 3])
    result = check_unique(non_unique_data)
    assert not result.is_valid
    assert "duplicate values" in result.message
    assert result.details["duplicate_count"] == 2


# Test check_monotonic function
def test_check_monotonic():
    # Test increasing data
    increasing_data = pd.Series([1, 2, 3, 4, 5])
    result = check_monotonic(increasing_data, increasing=True)
    assert result.is_valid
    assert "monotonically increasing" in result.message
    
    # Test decreasing data
    decreasing_data = pd.Series([5, 4, 3, 2, 1])
    result = check_monotonic(decreasing_data, increasing=False)
    assert result.is_valid
    assert "monotonically decreasing" in result.message
    
    # Test non-monotonic data
    non_monotonic_data = pd.Series([1, 3, 2, 4, 5])
    result = check_monotonic(non_monotonic_data, increasing=True)
    assert not result.is_valid
    assert "not monotonically increasing" in result.message
    assert result.details["violation_count"] == 1


# Test check_frequency function
def test_check_frequency():
    # Test matching frequencies
    data = pd.Series([1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
    expected_freq = {1: 0.18, 2: 0.18, 3: 0.27, 4: 0.36}
    result = check_frequency(data, expected_freq)
    assert result.is_valid
    assert "Frequencies match" in result.message
    
    # Test non-matching frequencies
    expected_freq = {1: 0.3, 2: 0.2, 3: 0.3, 4: 0.2}
    result = check_frequency(data, expected_freq)
    assert not result.is_valid
    assert "frequency deviations" in result.message
    assert len(result.details["deviations"]) > 0


# Test check_categorical function
def test_check_categorical(categorical_data):
    # Test with valid categories
    categories = ["apple", "banana", "orange"]
    result = check_categorical(categorical_data, categories)
    assert result.is_valid
    assert "All values belong to specified categories" in result.message
    
    # Test with invalid categories
    categories = ["apple", "banana"]
    result = check_categorical(categorical_data, categories)
    assert not result.is_valid
    assert "not in specified categories" in result.message
    assert result.details["invalid_count"] == 1
    assert "orange" in result.details["invalid_values"]


# Test check_string_length function
def test_check_string_length(categorical_data):
    # Test within length range
    result = check_string_length(categorical_data, min_length=5, max_length=6)
    assert result.is_valid
    assert "within range" in result.message
    
    # Test outside length range (min)
    result = check_string_length(categorical_data, min_length=6)
    assert not result.is_valid
    assert "String length validation failed" in result.message
    assert "too_short_count" in result.details
    
    # Test outside length range (max)
    result = check_string_length(categorical_data, max_length=5)
    assert not result.is_valid
    assert "String length validation failed" in result.message
    assert "too_long_count" in result.details


# Test check_pattern function
def test_check_pattern(categorical_data):
    # Test matching pattern
    result = check_pattern(categorical_data, r"^[a-z]+$")
    assert result.is_valid
    assert "All values match pattern" in result.message
    
    # Test non-matching pattern
    result = check_pattern(categorical_data, r"^[A-Z]+$")
    assert not result.is_valid
    assert "not matching pattern" in result.message
    assert result.details["non_matching_count"] == 5


# Test check_outliers function
def test_check_outliers():
    # Test data without outliers
    normal_data = pd.Series([1, 2, 3, 4, 5])
    result = check_outliers(normal_data, method='iqr')
    assert result.is_valid
    assert "No outliers detected" in result.message
    
    # Test data with outliers
    outlier_data = pd.Series([1, 2, 3, 4, 20])
    result = check_outliers(outlier_data, method='iqr')
    assert not result.is_valid
    assert "outliers" in result.message
    assert result.details["outlier_count"] == 1
    
    # Test different methods
    result = check_outliers(outlier_data, method='zscore')
    assert not result.is_valid
    assert "Z-Score" in result.details["method"]
    
    result = check_outliers(outlier_data, method='modified_zscore')
    assert not result.is_valid
    assert "Modified Z-Score" in result.details["method"]


# Test check_correlation function
def test_check_correlation():
    # Test positive correlation
    data1 = pd.Series([1, 2, 3, 4, 5])
    data2 = pd.Series([2, 4, 6, 8, 10])
    result = check_correlation(data1, data2, min_corr=0.9)
    assert result.is_valid
    assert "Correlation" in result.message
    assert result.details["correlation"] == 1.0
    
    # Test negative correlation
    data2 = pd.Series([10, 8, 6, 4, 2])
    result = check_correlation(data1, data2, max_corr=-0.9)
    assert result.is_valid
    assert result.details["correlation"] == -1.0
    
    # Test correlation outside range
    result = check_correlation(data1, data2, min_corr=0)
    assert not result.is_valid
    assert "outside specified range" in result.message


# Test Validator class
def test_validator_execute(numeric_data, numeric_data_with_nulls):
    # Test successful validation
    validator = Validator(check_positive, name="PositiveCheck")
    result = validator.execute(numeric_data)
    assert result is numeric_data  # Should return original data
    
    # Test failed validation
    validator = Validator(lambda x: check_range(x, 10, 20), name="RangeCheck")
    with pytest.raises(ValidationError):
        validator.execute(numeric_data)
    
    # Test last result
    assert validator.get_last_result() is not None
    assert not validator.get_last_result().is_valid


# Test Validator.combine method
def test_validator_combine(numeric_data, numeric_data_with_nulls):
    # Create validators
    positive_validator = Validator(check_positive, name="PositiveCheck")
    range_validator = Validator(lambda x: check_range(x, 1, 10), name="RangeCheck")
    null_validator = Validator(check_null, name="NullCheck")
    
    # Test all_must_pass=True with all passing
    combined = Validator.combine([positive_validator, range_validator], all_must_pass=True)
    result = combined.execute(numeric_data)
    assert result is numeric_data
    
    # Test all_must_pass=True with one failing
    combined = Validator.combine([positive_validator, null_validator], all_must_pass=True)
    with pytest.raises(ValidationError):
        combined.execute(numeric_data_with_nulls)
    
    # Test all_must_pass=False with one passing
    combined = Validator.combine([positive_validator, null_validator], all_must_pass=False)
    result = combined.execute(numeric_data_with_nulls)
    assert result is numeric_data_with_nulls