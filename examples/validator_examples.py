"""
Examples demonstrating the use of validators in dataDisk.
"""

import pandas as pd
import numpy as np
from dataDisk.validator import (
    ValidationResult, ValidationError, Validator,
    check_null, check_normal_dist, check_range, check_positive,
    check_unique, check_monotonic, check_frequency, check_categorical,
    check_string_length, check_pattern, check_outliers, check_correlation
)


# Example 1: Basic validation
def basic_validation_example():
    print("\nExample 1: Basic validation")
    
    # Create sample data
    data = pd.Series([1, 2, 3, 4, 5])
    print("Sample data:", data.tolist())
    
    # Check if all values are positive
    result = check_positive(data)
    print(f"Positive check: {result}")
    
    # Check if values are within range
    result = check_range(data, 0, 10)
    print(f"Range check: {result}")
    
    # Check if values are unique
    result = check_unique(data)
    print(f"Uniqueness check: {result}")
    
    # Try a failing check
    result = check_range(data, 2, 4)
    print(f"Range check (should fail): {result}")
    print(f"Failure details: {result.details}")


# Example 2: Using validators in a data pipeline
def pipeline_validation_example():
    print("\nExample 2: Using validators in a data pipeline")
    
    # Create sample data with issues
    data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'value': [10, -5, 30, np.nan, 50],
        'category': ['A', 'B', 'C', 'D', 'E']
    })
    print("Sample data:")
    print(data)
    
    # Create validators
    null_validator = Validator(check_null, name="NullCheck", 
                              error_message="Data contains null values")
    
    positive_validator = Validator(
        lambda x: check_positive(x['value']), 
        name="PositiveCheck",
        error_message="Values must be positive"
    )
    
    category_validator = Validator(
        lambda x: check_categorical(x['category'], ['A', 'B', 'C']),
        name="CategoryCheck",
        error_message="Invalid categories found"
    )
    
    # Try to validate the data
    print("\nValidating data...")
    
    try:
        # This will fail due to null values
        null_validator.execute(data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        print(f"Validation details: {null_validator.get_last_result().details}")
    
    # Fix the null values and try again
    print("\nFixing null values...")
    data = data.fillna(0)
    
    try:
        # This will fail due to negative values
        positive_validator.execute(data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        print(f"Validation details: {positive_validator.get_last_result().details}")
    
    # Fix the negative values and try again
    print("\nFixing negative values...")
    data['value'] = data['value'].abs()
    
    try:
        # This will fail due to invalid categories
        category_validator.execute(data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        print(f"Validation details: {category_validator.get_last_result().details}")
    
    # Fix the categories and try again
    print("\nFixing categories...")
    data.loc[data['category'].isin(['D', 'E']), 'category'] = 'C'
    
    # Now all validations should pass
    print("\nFinal validation:")
    try:
        null_validator.execute(data)
        positive_validator.execute(data)
        category_validator.execute(data)
        print("All validations passed!")
        print("Final data:")
        print(data)
    except ValidationError as e:
        print(f"Validation still failed: {e}")


# Example 3: Advanced validation with combined validators
def combined_validators_example():
    print("\nExample 3: Advanced validation with combined validators")
    
    # Create sample data
    np.random.seed(42)
    data = pd.DataFrame({
        'age': np.random.randint(18, 80, 100),
        'income': np.random.lognormal(10, 1, 100),
        'satisfaction': np.random.randint(1, 6, 100)
    })
    print("Sample data shape:", data.shape)
    print(data.describe())
    
    # Create individual validators
    age_validator = Validator(
        lambda x: check_range(x['age'], 18, 100),
        name="AgeRangeCheck"
    )
    
    income_validator = Validator(
        lambda x: check_outliers(x['income'], method='iqr'),
        name="IncomeOutlierCheck"
    )
    
    satisfaction_validator = Validator(
        lambda x: check_categorical(x['satisfaction'], [1, 2, 3, 4, 5]),
        name="SatisfactionCategoryCheck"
    )
    
    # Combine validators - all must pass
    all_validators = Validator.combine(
        [age_validator, income_validator, satisfaction_validator],
        all_must_pass=True
    )
    
    # Try to validate
    try:
        all_validators.execute(data)
        print("All validations passed!")
    except ValidationError as e:
        print(f"Validation failed: {e}")
        result = all_validators.get_last_result()
        print(f"Failed validators: {result.details['failed']}")
        
    # Add some outliers to the data
    data.loc[0, 'income'] = 1000000  # Extreme value
    
    # Try to validate again
    try:
        all_validators.execute(data)
        print("All validations passed!")
    except ValidationError as e:
        print(f"Validation failed: {e}")
        result = all_validators.get_last_result()
        print(f"Failed validators: {result.details['failed']}")
        
    # Create a combined validator where any can pass
    any_validator = Validator.combine(
        [age_validator, satisfaction_validator],
        all_must_pass=False
    )
    
    # This should pass since at least one validator passes
    try:
        any_validator.execute(data)
        print("At least one validation passed!")
        result = any_validator.get_last_result()
        print(f"Passed validators: {result.details['passed']}")
    except ValidationError as e:
        print(f"All validations failed: {e}")


# Example 4: Statistical validation
def statistical_validation_example():
    print("\nExample 4: Statistical validation")
    
    # Create normally distributed data
    np.random.seed(42)
    normal_data = pd.DataFrame({
        'normal': np.random.normal(0, 1, 100),
        'uniform': np.random.uniform(-1, 1, 100),
        'exponential': np.random.exponential(1, 100)
    })
    
    print("Sample data statistics:")
    print(normal_data.describe())
    
    # Check for normal distribution
    for column in normal_data.columns:
        result = check_normal_dist(normal_data[column])
        print(f"\nNormality check for {column}: {result.is_valid}")
        print(f"p-value: {result.details['p_value']:.4f}")
        print(f"skewness: {result.details['skewness']:.4f}")
        print(f"kurtosis: {result.details['kurtosis']:.4f}")
    
    # Check for correlations
    print("\nCorrelation checks:")
    for col1 in normal_data.columns:
        for col2 in normal_data.columns:
            if col1 != col2:
                result = check_correlation(normal_data[col1], normal_data[col2])
                print(f"{col1} vs {col2}: {result.details['correlation']:.4f}")
    
    # Check for outliers
    print("\nOutlier checks:")
    for column in normal_data.columns:
        for method in ['iqr', 'zscore', 'modified_zscore']:
            result = check_outliers(normal_data[column], method=method)
            status = "PASSED" if result.is_valid else "FAILED"
            outlier_count = result.details.get('outlier_count', 0)
            print(f"{column} ({method}): {status} - {outlier_count} outliers")


if __name__ == "__main__":
    basic_validation_example()
    pipeline_validation_example()
    combined_validators_example()
    statistical_validation_example()
    
    print("\nAll examples completed.")