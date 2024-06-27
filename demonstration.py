import pandas as pd
from dataDisk.transformation import Transformation

# Sample data
data = pd.DataFrame({
    'A': [1, 2, 3, 4, None],
    'B': [5, 6, 7, None, 9],
    'C': ['X', 'Y', 'X', 'Z', 'Z'],
    'D': [10, 11, None, 13, 14],
    'E': [10, 11, None, 13, 14]
})

# Data cleaning
cleaner = Transformation(Transformation.data_cleaning)
cleaned_data = cleaner.execute(data)
print("Cleaned Data:")
print(cleaned_data)
print()

# Impute missing values
imputer = Transformation(Transformation.impute_missing)
imputed_data = imputer.execute(data)
print("Imputed Data:")
print(imputed_data)
print()

# Log transformation
log_transformer = Transformation(Transformation.log_transform)
log_transformed_data = log_transformer.execute(data['A'].values)
print("Log Transformed Data:")
print(log_transformed_data)
print()

# Binning
binner = Transformation(Transformation.binning)
binned_data = binner.execute(data['B'].values, num_bins=3)
print("Binned Data:")
print(binned_data)
print()

# Interaction terms
interaction_transformer = Transformation(Transformation.interaction_terms)
interaction_data = interaction_transformer.execute(data[['A', 'B']].values)
print("Interaction Data:")
print(interaction_data)
print()

# Polynomial features
poly_transformer = Transformation(Transformation.polynomial_features)
poly_features_data = poly_transformer.execute(
    data[['A', 'B']].values, degree=2)
print("Polynomial Features Data:")
print(poly_features_data)
print()
