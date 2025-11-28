import logging
import re
from typing import Callable, Dict, List, Union, Optional, Any, Tuple
import pandas as pd
import numpy as np
from pandas import isna, Series, DataFrame
from scipy.stats import shapiro, skew, kurtosis


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ValidationResult:
    """
    Class to store validation results with detailed information.
    """
    
    def __init__(self, is_valid: bool, message: str = "", details: Dict = None):
        """
        Initialize validation result.
        
        Args:
            is_valid: Whether validation passed
            message: Message describing the validation result
            details: Additional details about the validation
        """
        self.is_valid = is_valid
        self.message = message
        self.details = details or {}
        
    def __bool__(self):
        """Allow using the result in boolean context."""
        return self.is_valid
        
    def __str__(self):
        """String representation of the validation result."""
        status = "PASSED" if self.is_valid else "FAILED"
        return f"Validation {status}: {self.message}"


def check_null(data: Union[Series, DataFrame]) -> ValidationResult:
    """
    Checks for null values in the data.

    Args:
        data: The data to check for null values

    Returns:
        ValidationResult indicating if validation passed
    """
    is_valid = not isna(data).any().any() if isinstance(data, DataFrame) else not isna(data).any()
    
    if is_valid:
        return ValidationResult(True, "No null values found")
    else:
        null_count = isna(data).sum().sum() if isinstance(data, DataFrame) else isna(data).sum()
        details = {"null_count": int(null_count)}
        
        if isinstance(data, DataFrame):
            null_columns = data.columns[data.isna().any()].tolist()
            details["null_columns"] = null_columns
            
        return ValidationResult(False, f"Found {null_count} null values", details)


def check_normal_dist(data: Series, alpha: float = 0.05) -> ValidationResult:
    """
    Checks if data follows a normal distribution using the Shapiro-Wilk test.

    Args:
        data: The data to check for normal distribution
        alpha: The significance level for the Shapiro-Wilk test

    Returns:
        ValidationResult indicating if validation passed
    """
    # Drop NaN values for the test
    clean_data = data.dropna()
    
    if len(clean_data) < 3:
        return ValidationResult(False, "Not enough data points for normality test")
        
    stat, p_value = shapiro(clean_data)
    is_valid = p_value > alpha
    
    details = {
        "statistic": float(stat),
        "p_value": float(p_value),
        "alpha": alpha,
        "skewness": float(skew(clean_data)),
        "kurtosis": float(kurtosis(clean_data))
    }
    
    if is_valid:
        return ValidationResult(True, "Data follows normal distribution", details)
    else:
        return ValidationResult(False, "Data does not follow normal distribution", details)


def check_range(data: Series, min_val: float, max_val: float) -> ValidationResult:
    """
    Checks if data is within a given min-max range.

    Args:
        data: The data to check
        min_val: The minimum value of the range
        max_val: The maximum value of the range

    Returns:
        ValidationResult indicating if validation passed
    """
    # Drop NaN values for the check
    clean_data = data.dropna()
    
    min_check = (clean_data >= min_val).all()
    max_check = (clean_data <= max_val).all()
    is_valid = min_check and max_check
    
    details = {
        "actual_min": float(clean_data.min()),
        "actual_max": float(clean_data.max()),
        "expected_min": float(min_val),
        "expected_max": float(max_val)
    }
    
    if not min_check:
        below_min = clean_data[clean_data < min_val]
        details["below_min_count"] = len(below_min)
        details["below_min_values"] = below_min.tolist()
        
    if not max_check:
        above_max = clean_data[clean_data > max_val]
        details["above_max_count"] = len(above_max)
        details["above_max_values"] = above_max.tolist()
    
    if is_valid:
        return ValidationResult(True, f"All values are within range [{min_val}, {max_val}]", details)
    else:
        return ValidationResult(False, f"Values outside range [{min_val}, {max_val}]", details)


def check_positive(data: Series) -> ValidationResult:
    """
    Checks if all data values are positive.

    Args:
        data: The data to check

    Returns:
        ValidationResult indicating if validation passed
    """
    # Drop NaN values for the check
    clean_data = data.dropna()
    
    is_valid = (clean_data > 0).all()
    
    details = {
        "min_value": float(clean_data.min()),
        "negative_count": int((clean_data <= 0).sum())
    }
    
    if not is_valid:
        non_positive = clean_data[clean_data <= 0]
        details["non_positive_values"] = non_positive.tolist()
    
    if is_valid:
        return ValidationResult(True, "All values are positive", details)
    else:
        return ValidationResult(False, f"Found {details['negative_count']} non-positive values", details)


def check_unique(data: Series) -> ValidationResult:
    """
    Checks if all data values are unique.

    Args:
        data: The data to check

    Returns:
        ValidationResult indicating if validation passed
    """
    # Drop NaN values for the check
    clean_data = data.dropna()
    
    is_valid = clean_data.is_unique
    
    if is_valid:
        return ValidationResult(True, "All values are unique")
    else:
        duplicates = clean_data[clean_data.duplicated()]
        duplicate_values = duplicates.tolist()
        duplicate_counts = clean_data.value_counts()[clean_data.value_counts() > 1].to_dict()
        
        details = {
            "duplicate_count": len(duplicate_values),
            "duplicate_values": duplicate_values,
            "value_counts": duplicate_counts
        }
        
        return ValidationResult(False, f"Found {len(duplicate_values)} duplicate values", details)


def check_monotonic(data: Series, increasing: bool = True) -> ValidationResult:
    """
    Checks if data values are monotonically increasing or decreasing.

    Args:
        data: The data to check
        increasing: Set to True to check for increasing order, False for decreasing order

    Returns:
        ValidationResult indicating if validation passed
    """
    # Drop NaN values for the check
    clean_data = data.dropna()
    
    if increasing:
        is_valid = clean_data.is_monotonic_increasing
        direction = "increasing"
    else:
        is_valid = clean_data.is_monotonic_decreasing
        direction = "decreasing"
    
    if is_valid:
        return ValidationResult(True, f"Data is monotonically {direction}")
    else:
        # Find violations
        if increasing:
            violations = [(i, clean_data.iloc[i], clean_data.iloc[i+1]) 
                         for i in range(len(clean_data)-1) 
                         if clean_data.iloc[i] > clean_data.iloc[i+1]]
        else:
            violations = [(i, clean_data.iloc[i], clean_data.iloc[i+1]) 
                         for i in range(len(clean_data)-1) 
                         if clean_data.iloc[i] < clean_data.iloc[i+1]]
        
        details = {
            "violation_count": len(violations),
            "violations": violations[:10]  # Limit to first 10 violations
        }
        
        return ValidationResult(False, f"Data is not monotonically {direction}", details)


def check_frequency(data: Series, expected_freq: Dict, tolerance: float = 0.05) -> ValidationResult:
    """
    Checks if the frequency of data values matches the expected frequency within a given tolerance.

    Args:
        data: The data to check
        expected_freq: A dictionary with expected frequencies for each value
        tolerance: The tolerance for frequency deviation

    Returns:
        ValidationResult indicating if validation passed
    """
    actual_freq = data.value_counts(normalize=True).to_dict()
    
    deviations = {}
    for value, freq in expected_freq.items():
        actual = actual_freq.get(value, 0)
        deviation = abs(actual - freq)
        if deviation > tolerance:
            deviations[value] = {
                "expected": freq,
                "actual": actual,
                "deviation": deviation
            }
    
    is_valid = len(deviations) == 0
    
    details = {
        "expected_frequencies": expected_freq,
        "actual_frequencies": actual_freq,
        "tolerance": tolerance
    }
    
    if not is_valid:
        details["deviations"] = deviations
    
    if is_valid:
        return ValidationResult(True, "Frequencies match expected values within tolerance", details)
    else:
        return ValidationResult(False, f"Found {len(deviations)} frequency deviations exceeding tolerance", details)


def check_categorical(data: Series, categories: List) -> ValidationResult:
    """
    Checks if all data values belong to a set of specified categories.

    Args:
        data: The data to check
        categories: The list of valid categories

    Returns:
        ValidationResult indicating if validation passed
    """
    is_valid = data.isin(categories).all()
    
    if is_valid:
        return ValidationResult(True, "All values belong to specified categories")
    else:
        invalid_values = data[~data.isin(categories)].unique().tolist()
        details = {
            "invalid_count": len(invalid_values),
            "invalid_values": invalid_values,
            "valid_categories": categories
        }
        
        return ValidationResult(False, f"Found {len(invalid_values)} values not in specified categories", details)


def check_string_length(data: Series, min_length: Optional[int] = None, 
                       max_length: Optional[int] = None) -> ValidationResult:
    """
    Checks if the length of string data is within the specified range.

    Args:
        data: The data to check
        min_length: The minimum length of the strings
        max_length: The maximum length of the strings

    Returns:
        ValidationResult indicating if validation passed
    """
    lengths = data.str.len()
    
    min_check = True
    max_check = True
    
    if min_length is not None:
        min_check = (lengths >= min_length).all()
    
    if max_length is not None:
        max_check = (lengths <= max_length).all()
    
    is_valid = min_check and max_check
    
    details = {
        "min_length": min_length,
        "max_length": max_length,
        "actual_min_length": int(lengths.min()),
        "actual_max_length": int(lengths.max())
    }
    
    if not min_check:
        too_short = data[lengths < min_length]
        details["too_short_count"] = len(too_short)
        details["too_short_values"] = too_short.tolist()
    
    if not max_check:
        too_long = data[lengths > max_length]
        details["too_long_count"] = len(too_long)
        details["too_long_values"] = too_long.tolist()
    
    if is_valid:
        range_str = ""
        if min_length is not None and max_length is not None:
            range_str = f"[{min_length}, {max_length}]"
        elif min_length is not None:
            range_str = f">= {min_length}"
        elif max_length is not None:
            range_str = f"<= {max_length}"
            
        return ValidationResult(True, f"All string lengths are within range {range_str}", details)
    else:
        return ValidationResult(False, "String length validation failed", details)


def check_pattern(data: Series, pattern: str) -> ValidationResult:
    """
    Checks if all data values match a given regular expression pattern.

    Args:
        data: The data to check
        pattern: The regular expression pattern to match

    Returns:
        ValidationResult indicating if validation passed
    """
    matches = data.str.match(pattern)
    is_valid = matches.all()
    
    if is_valid:
        return ValidationResult(True, f"All values match pattern '{pattern}'")
    else:
        non_matching = data[~matches]
        details = {
            "non_matching_count": len(non_matching),
            "non_matching_values": non_matching.tolist(),
            "pattern": pattern
        }
        
        return ValidationResult(False, f"Found {len(non_matching)} values not matching pattern", details)


def check_outliers(data: Series, method: str = 'iqr', threshold: float = 1.5) -> ValidationResult:
    """
    Checks for outliers in the data using various methods.

    Args:
        data: The data to check
        method: Method to use ('iqr', 'zscore', 'modified_zscore')
        threshold: Threshold for outlier detection

    Returns:
        ValidationResult indicating if validation passed
    """
    clean_data = data.dropna()
    
    outliers = []
    if method == 'iqr':
        q1 = clean_data.quantile(0.25)
        q3 = clean_data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)]
        
        details = {
            "method": "IQR",
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound)
        }
        
    elif method == 'zscore':
        mean = clean_data.mean()
        std = clean_data.std()
        zscores = (clean_data - mean) / std
        outliers = clean_data[abs(zscores) > threshold]
        
        details = {
            "method": "Z-Score",
            "mean": float(mean),
            "std": float(std),
            "threshold": threshold
        }
        
    elif method == 'modified_zscore':
        median = clean_data.median()
        mad = (clean_data - median).abs().median() * 1.4826  # Consistent with normal distribution
        modified_zscores = 0.6745 * (clean_data - median) / mad
        outliers = clean_data[abs(modified_zscores) > threshold]
        
        details = {
            "method": "Modified Z-Score",
            "median": float(median),
            "mad": float(mad),
            "threshold": threshold
        }
    
    is_valid = len(outliers) == 0
    
    if not is_valid:
        details["outlier_count"] = len(outliers)
        details["outlier_values"] = outliers.tolist()
    
    if is_valid:
        return ValidationResult(True, f"No outliers detected using {method} method", details)
    else:
        return ValidationResult(False, f"Found {len(outliers)} outliers using {method} method", details)


def check_correlation(data1: Series, data2: Series, 
                     min_corr: Optional[float] = None, 
                     max_corr: Optional[float] = None) -> ValidationResult:
    """
    Checks if correlation between two series is within specified range.

    Args:
        data1: First data series
        data2: Second data series
        min_corr: Minimum correlation value
        max_corr: Maximum correlation value

    Returns:
        ValidationResult indicating if validation passed
    """
    # Drop rows where either series has NaN
    clean_data = pd.DataFrame({'data1': data1, 'data2': data2}).dropna()
    
    if len(clean_data) < 2:
        return ValidationResult(False, "Not enough data points to calculate correlation")
    
    corr = clean_data['data1'].corr(clean_data['data2'])
    
    min_check = True
    max_check = True
    
    if min_corr is not None:
        min_check = corr >= min_corr
    
    if max_corr is not None:
        max_check = corr <= max_corr
    
    is_valid = min_check and max_check
    
    details = {
        "correlation": float(corr),
        "min_correlation": min_corr,
        "max_correlation": max_corr,
        "sample_size": len(clean_data)
    }
    
    if is_valid:
        return ValidationResult(True, f"Correlation ({corr:.4f}) is within specified range", details)
    else:
        return ValidationResult(False, f"Correlation ({corr:.4f}) is outside specified range", details)


class Validator:
    """
    A class to validate data based on user-defined criteria.
    """

    def __init__(self, validate_func: Callable, name: Optional[str] = None, 
                error_message: Optional[str] = None):
        """
        Initialize validator with a validation function.
        
        Args:
            validate_func: Function that takes data and returns ValidationResult or bool
            name: Optional name for the validator
            error_message: Custom error message on validation failure
        """
        self.validate_func = validate_func
        self.name = name or getattr(validate_func, '__name__', 'unknown_validator')
        self.error_message = error_message or "Data validation failed"
        self.last_result = None

    def execute(self, data: Any) -> Any:
        """
        Execute the validation function on the provided data.

        Args:
            data: The data to validate

        Returns:
            The original data if validation passes

        Raises:
            ValidationError: If the data fails validation
        """
        try:
            logging.info(f"Executing validator: {self.name}")
            
            # Call the validation function
            result = self.validate_func(data)
            
            # Convert boolean result to ValidationResult if needed
            if isinstance(result, bool):
                result = ValidationResult(result, 
                                         "Validation passed" if result else self.error_message)
            
            self.last_result = result
            
            if result.is_valid:
                logging.info(f"Validation passed: {result.message}")
                return data
            else:
                error_msg = f"{self.error_message}: {result.message}"
                logging.error(error_msg)
                raise ValidationError(error_msg)
                
        except ValidationError:
            raise
        except Exception as e:
            error_msg = f"Error during validation '{self.name}': {str(e)}"
            logging.error(error_msg)
            raise ValidationError(error_msg) from e
    
    def get_last_result(self) -> Optional[ValidationResult]:
        """Get the result of the last validation."""
        return self.last_result
    
    @classmethod
    def combine(cls, validators: List['Validator'], all_must_pass: bool = True) -> 'Validator':
        """
        Combine multiple validators into a single validator.
        
        Args:
            validators: List of validators to combine
            all_must_pass: If True, all validators must pass; if False, at least one must pass
            
        Returns:
            A new validator that combines the given validators
        """
        def combined_validate(data):
            results = []
            passed = []
            failed = []
            
            for validator in validators:
                try:
                    result = validator.validate_func(data)
                    
                    # Convert boolean result to ValidationResult if needed
                    if isinstance(result, bool):
                        result = ValidationResult(result, 
                                                "Validation passed" if result else "Validation failed")
                    
                    results.append(result)
                    if result.is_valid:
                        passed.append(validator.name)
                    else:
                        failed.append(validator.name)
                        
                except Exception as e:
                    failed.append(validator.name)
                    results.append(ValidationResult(False, str(e)))
            
            if all_must_pass:
                is_valid = all(result.is_valid for result in results)
                mode = "ALL"
            else:
                is_valid = any(result.is_valid for result in results)
                mode = "ANY"
            
            details = {
                "mode": mode,
                "validators_total": len(validators),
                "validators_passed": len(passed),
                "validators_failed": len(failed),
                "passed": passed,
                "failed": failed
            }
            
            if is_valid:
                return ValidationResult(True, f"Combined validation passed ({mode} mode)", details)
            else:
                return ValidationResult(False, f"Combined validation failed ({mode} mode)", details)
        
        validator_names = [v.name for v in validators]
        name = f"Combined({','.join(validator_names)})"
        return cls(combined_validate, name=name)
