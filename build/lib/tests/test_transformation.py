import pytest
import pandas as pd
import numpy as np
from dataDisk.transformation import Transformation, TransformationError


# Create sample data for testing
@pytest.fixture
def numeric_data():
    return pd.DataFrame({
        'A': [1, 2, np.nan, 4],
        'B': [5.0, np.nan, 7.0, 8.0],
        'C': [9, 10, 11, 12]
    })


@pytest.fixture
def categorical_data():
    return pd.DataFrame({
        'Category': ['A', 'B', 'A', 'B'],
        'Value': [1, 2, 3, 4],
        'Group': ['X', 'Y', 'X', 'Z']
    })


@pytest.fixture
def mixed_data():
    return pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5],
        'numeric2': [10.5, 20.5, 30.5, 40.5, 50.5],
        'category1': ['A', 'B', 'C', 'A', 'B'],
        'category2': ['X', 'X', 'Y', 'Z', 'Y'],
        'with_missing': [1.0, np.nan, 3.0, np.nan, 5.0]
    })


# Test basic transformation functionality
def test_transformation_init():
    def double(x):
        return x * 2
    
    transform = Transformation(double, name="Double")
    assert transform.name == "Double"
    assert transform.func == double
    
    # Test with default name
    transform2 = Transformation(double)
    assert transform2.name == "double"


def test_transformation_execute():
    def add_one(x):
        return x + 1
    
    transform = Transformation(add_one)
    result = transform.execute(5)
    assert result == 6


def test_transformation_error():
    def problematic_func(x):
        raise ValueError("Test error")
    
    transform = Transformation(problematic_func)
    with pytest.raises(TransformationError):
        transform.execute(5)


def test_transformation_metadata():
    transform = Transformation(lambda x: x * 2, name="Double")
    transform.set_metadata("description", "Doubles the input")
    transform.set_metadata("author", "Test User")
    
    assert transform.get_metadata("description") == "Doubles the input"
    assert transform.get_metadata("author") == "Test User"
    assert transform.get_metadata() == {
        "description": "Doubles the input",
        "author": "Test User"
    }


def test_transformation_chain():
    t1 = Transformation(lambda x: x + 1, name="AddOne")
    t2 = Transformation(lambda x: x * 2, name="Double")
    t3 = Transformation(lambda x: x - 3, name="SubThree")
    
    chain = Transformation.chain([t1, t2, t3])
    result = chain.execute(5)
    
    # (5 + 1) * 2 - 3 = 9
    assert result == 9
    assert "Chain" in chain.get_name()
    assert "AddOne" in chain.get_name()
    assert "Double" in chain.get_name()
    assert "SubThree" in chain.get_name()


# Test specific transformations
def test_standardize(numeric_data):
    result = Transformation.standardize(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check NaN values are handled
    assert not result.isna().any().any()
    
    # Check standardization (mean should be close to 0, std close to 1)
    for col in result.columns:
        assert abs(result[col].mean()) < 0.01
        assert abs(result[col].std() - 1.0) < 0.01


def test_normalize(numeric_data):
    result = Transformation.normalize(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check NaN values are handled
    assert not result.isna().any().any()


def test_min_max_scale(numeric_data):
    result = Transformation.min_max_scale(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check NaN values are handled
    assert not result.isna().any().any()
    
    # Check values are in [0, 1] range
    for col in result.columns:
        assert result[col].min() >= 0
        assert result[col].max() <= 1


def test_label_encode(categorical_data):
    result = Transformation.label_encode(categorical_data)
    
    # Check shape is preserved
    assert result.shape == categorical_data.shape
    
    # Check categorical columns are encoded as numbers
    assert result['Category'].dtype in [np.int64, np.int32]
    assert result['Group'].dtype in [np.int64, np.int32]
    
    # Check unique values are preserved
    assert len(result['Category'].unique()) == len(categorical_data['Category'].unique())
    assert len(result['Group'].unique()) == len(categorical_data['Group'].unique())


def test_onehot_encode(categorical_data):
    result = Transformation.onehot_encode(categorical_data)
    
    # Check categorical columns are dropped
    assert 'Category' not in result.columns
    assert 'Group' not in result.columns
    
    # Check one-hot columns are created
    assert 'Category_A' in result.columns
    assert 'Category_B' in result.columns
    assert 'Group_X' in result.columns
    assert 'Group_Y' in result.columns
    assert 'Group_Z' in result.columns
    
    # Check numeric column is preserved
    assert 'Value' in result.columns


def test_data_cleaning(mixed_data):
    result = Transformation.data_cleaning(mixed_data)
    
    # Check shape is preserved
    assert result.shape[0] == mixed_data.shape[0]
    
    # Check missing values are handled
    assert not result.isna().any().any()
    
    # Check categorical columns are encoded
    assert result['category1'].dtype in [np.int64, np.int32]
    assert result['category2'].dtype in [np.int64, np.int32]


def test_impute_missing(numeric_data):
    # Test mean imputation
    result_mean = Transformation.impute_missing(numeric_data, strategy='mean')
    assert not result_mean.isna().any().any()
    
    # Test median imputation
    result_median = Transformation.impute_missing(numeric_data, strategy='median')
    assert not result_median.isna().any().any()
    
    # Test KNN imputation
    result_knn = Transformation.impute_missing(numeric_data, strategy='knn')
    assert not result_knn.isna().any().any()


def test_log_transform(numeric_data):
    result = Transformation.log_transform(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check values are log-transformed
    for col in result.columns:
        non_nan_original = numeric_data[col].dropna()
        non_nan_result = result[col].dropna()
        if len(non_nan_original) > 0:
            assert np.allclose(non_nan_result, np.log1p(non_nan_original))


def test_sqrt_transform(numeric_data):
    result = Transformation.sqrt_transform(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check NaN values are handled
    assert not result.isna().any().any()
    
    # Check values are sqrt-transformed
    for col in result.columns:
        non_nan_original = numeric_data[col].fillna(0)
        assert np.allclose(result[col], np.sqrt(non_nan_original))


def test_robust_scale(numeric_data):
    result = Transformation.robust_scale(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check NaN values are handled
    assert not result.isna().any().any()


def test_binning(numeric_data):
    result = Transformation.binning(numeric_data['C'], num_bins=3)
    
    # Check shape is preserved
    assert len(result) == len(numeric_data['C'])
    
    # Check number of unique bins
    assert len(pd.Series(result).unique()) <= 3


def test_interaction_terms(numeric_data):
    result = Transformation.interaction_terms(numeric_data)
    
    # Check more columns are created
    assert result.shape[1] > numeric_data.shape[1]
    
    # Check original columns are preserved
    for col in numeric_data.columns:
        assert col in result.columns


def test_polynomial_features(numeric_data):
    result = Transformation.polynomial_features(numeric_data, degree=2)
    
    # Check more columns are created
    assert result.shape[1] > numeric_data.shape[1]
    
    # Check squared terms exist
    assert 'A^2' in result.columns or 'A**2' in result.columns


def test_pca_transform(numeric_data):
    # Fill NaN values for this test
    filled_data = numeric_data.fillna(numeric_data.mean())
    
    # Test with specific number of components
    result1 = Transformation.pca_transform(filled_data, n_components=2)
    assert result1.shape[1] == 2
    assert 'PC1' in result1.columns
    assert 'PC2' in result1.columns
    
    # Test with variance threshold
    result2 = Transformation.pca_transform(filled_data, variance_threshold=0.99)
    assert result2.shape[1] <= filled_data.shape[1]


def test_feature_selection(mixed_data):
    # Create a target variable
    target = mixed_data['numeric1'] * 2 + mixed_data['numeric2']
    
    # Select features
    features = mixed_data.drop('numeric1', axis=1)  # Drop one to make it interesting
    result = Transformation.feature_selection(features, target, k=2)
    
    # Check we get exactly k features
    assert result.shape[1] == 2


def test_power_transform(numeric_data):
    result = Transformation.power_transform(numeric_data)
    
    # Check shape is preserved
    assert result.shape == numeric_data.shape
    
    # Check NaN values are handled
    assert not result.isna().any().any()