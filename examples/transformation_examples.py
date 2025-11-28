"""
Examples demonstrating the use of transformations in dataDisk.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataDisk.transformation import Transformation


# Create sample data
def create_sample_data(rows=100):
    np.random.seed(42)
    
    data = pd.DataFrame({
        'id': range(1, rows + 1),
        'age': np.random.normal(35, 10, rows).astype(int),
        'income': np.random.lognormal(10, 1, rows),
        'education_years': np.random.randint(8, 22, rows),
        'gender': np.random.choice(['M', 'F'], rows),
        'region': np.random.choice(['North', 'South', 'East', 'West'], rows),
        'satisfaction': np.random.randint(1, 6, rows)
    })
    
    # Add some missing values
    for col in ['age', 'income', 'education_years']:
        mask = np.random.random(rows) < 0.05
        data.loc[mask, col] = np.nan
        
    return data


# Example 1: Basic transformations
def basic_transformations_example():
    print("\nExample 1: Basic transformations")
    
    # Create sample data
    data = create_sample_data(10)
    print("Original data:")
    print(data.head())
    
    # Create a simple transformation
    def add_age_group(df):
        df = df.copy()
        bins = [0, 18, 30, 50, 100]
        labels = ['<18', '18-30', '31-50', '50+']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
        return df
    
    # Create transformation object
    age_group_transform = Transformation(add_age_group, name="AddAgeGroup")
    
    # Apply transformation
    result = age_group_transform.execute(data)
    
    print("\nData after adding age groups:")
    print(result[['id', 'age', 'age_group']].head())
    
    # Apply standardization to numeric columns
    std_transform = Transformation(Transformation.standardize, name="Standardize")
    result = std_transform.execute(result)
    
    print("\nData after standardization:")
    print(result[['age', 'income', 'education_years']].head())
    print(f"Mean of age: {result['age'].mean():.4f}")
    print(f"Std of age: {result['age'].std():.4f}")


# Example 2: Chaining transformations
def chaining_transformations_example():
    print("\nExample 2: Chaining transformations")
    
    # Create sample data
    data = create_sample_data(10)
    print("Original data:")
    print(data.head())
    
    # Create individual transformations
    impute_transform = Transformation(
        lambda df: Transformation.impute_missing(df, strategy='median'),
        name="ImputeMissing"
    )
    
    scale_transform = Transformation(
        lambda df: Transformation.min_max_scale(df),
        name="MinMaxScale"
    )
    
    encode_transform = Transformation(
        lambda df: Transformation.onehot_encode(df),
        name="OneHotEncode"
    )
    
    # Chain transformations
    pipeline_transform = Transformation.chain([
        impute_transform,
        scale_transform,
        encode_transform
    ])
    
    # Apply chained transformation
    result = pipeline_transform.execute(data)
    
    print("\nData after chained transformations:")
    print(result.head())
    print(f"Number of columns before: {data.shape[1]}, after: {result.shape[1]}")
    
    # Check for missing values
    print(f"Missing values before: {data.isna().sum().sum()}")
    print(f"Missing values after: {result.isna().sum().sum()}")


# Example 3: Advanced feature engineering
def advanced_feature_engineering_example():
    print("\nExample 3: Advanced feature engineering")
    
    # Create larger sample data
    data = create_sample_data(100)
    
    # Create a target variable for demonstration
    data['target'] = data['income'] / 1000 + data['education_years'] * 2 + np.random.normal(0, 10, len(data))
    
    print("Original data shape:", data.shape)
    
    # 1. Clean and prepare data
    clean_data = Transformation.data_cleaning(data)
    print("Data after cleaning shape:", clean_data.shape)
    
    # 2. Create polynomial features for numeric columns
    numeric_cols = ['age', 'income', 'education_years']
    poly_data = Transformation.polynomial_features(
        clean_data[numeric_cols], 
        degree=2
    )
    
    # Combine with original data
    combined_data = pd.concat([clean_data.drop(numeric_cols, axis=1), poly_data], axis=1)
    print("Data after polynomial features shape:", combined_data.shape)
    
    # 3. Create interaction terms
    interaction_data = Transformation.interaction_terms(combined_data.select_dtypes(include=['float64', 'int64']))
    
    # Combine with original data
    final_data = pd.concat([combined_data, interaction_data], axis=1)
    print("Data after interaction terms shape:", final_data.shape)
    
    # 4. Select top features
    target = data['target']
    selected_features = Transformation.feature_selection(final_data.drop('target', axis=1), target, k=10)
    print("\nTop 10 selected features:")
    print(selected_features.columns.tolist())
    
    # 5. Apply PCA for visualization
    pca_result = Transformation.pca_transform(selected_features, n_components=2)
    
    # Plot PCA results
    plt.figure(figsize=(10, 6))
    plt.scatter(pca_result['PC1'], pca_result['PC2'], c=target, cmap='viridis', alpha=0.7)
    plt.colorbar(label='Target Value')
    plt.title('PCA Visualization of Selected Features')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.savefig('pca_visualization.png')
    print("\nPCA visualization saved to 'pca_visualization.png'")


# Example 4: Custom transformation classes
def custom_transformation_example():
    print("\nExample 4: Custom transformation classes")
    
    # Create sample data
    data = create_sample_data(10)
    
    # Define a custom transformation function with metadata
    def income_to_category(df):
        df = df.copy()
        bins = [0, 20000, 50000, 100000, float('inf')]
        labels = ['Low', 'Medium', 'High', 'Very High']
        df['income_category'] = pd.cut(df['income'], bins=bins, labels=labels)
        return df
    
    # Create transformation with metadata
    income_transform = Transformation(income_to_category, name="IncomeCategories")
    income_transform.set_metadata("description", "Categorizes income into brackets")
    income_transform.set_metadata("bins", [0, 20000, 50000, 100000, float('inf')])
    income_transform.set_metadata("labels", ['Low', 'Medium', 'High', 'Very High'])
    
    # Apply transformation
    result = income_transform.execute(data)
    
    print("Data with income categories:")
    print(result[['id', 'income', 'income_category']].head())
    
    # Print metadata
    print("\nTransformation metadata:")
    for key, value in income_transform.get_metadata().items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    basic_transformations_example()
    chaining_transformations_example()
    advanced_feature_engineering_example()
    custom_transformation_example()
    
    print("\nAll examples completed.")