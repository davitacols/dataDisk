import logging
import pandas as pd
from dataDisk.transformation import Transformation

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a sample dataset
data = {
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [6, 7, 8, 9, 10],
    'category': ['A', 'B', 'A', 'B', 'A'],
    'feature3': [None, 2, None, 4, 5]
}
df = pd.DataFrame(data)

# Print the original data
logging.info("Original Data:")
logging.info(df.head())

# Test standardize transformation
logging.info("Testing standardize transformation")
df_standardized = Transformation.standardize(df.copy())
logging.info(df_standardized.head())

# Test normalize transformation
logging.info("Testing normalize transformation")
df_normalized = Transformation.normalize(df.copy())
logging.info(df_normalized.head())

# Test label_encode transformation
logging.info("Testing label_encode transformation")
df_label_encoded = Transformation.label_encode(df.copy())
logging.info(df_label_encoded.head())

# Test onehot_encode transformation
logging.info("Testing onehot_encode transformation")
df_onehot_encoded = Transformation.onehot_encode(df.copy())
logging.info(df_onehot_encoded.head())

# Test data_cleaning transformation
logging.info("Testing data_cleaning transformation")
df_cleaned = Transformation.data_cleaning(df.copy())
logging.info(df_cleaned.head())

# Test log_transform transformation
logging.info("Testing log_transform transformation")
df_log_transformed = df.copy()
df_log_transformed['feature1'] = Transformation.log_transform(df_log_transformed['feature1'])
logging.info(df_log_transformed.head())

# Test sqrt_transform transformation
logging.info("Testing sqrt_transform transformation")
df_sqrt_transformed = df.copy()
df_sqrt_transformed['feature1'] = Transformation.sqrt_transform(df_sqrt_transformed['feature1'])
logging.info(df_sqrt_transformed.head())

# Test robust_scale transformation
logging.info("Testing robust_scale transformation")
df_robust_scaled = Transformation.robust_scale(df.copy())
logging.info(df_robust_scaled.head())

# Test binning transformation
logging.info("Testing binning transformation")
df_binned = df.copy()
df_binned['feature1'] = Transformation.binning(df_binned['feature1'], num_bins=3)
logging.info(df_binned.head())

# Test interaction_terms transformation
logging.info("Testing interaction_terms transformation")
df_interaction_terms = Transformation.interaction_terms(df[['feature1', 'feature2']].copy())
df_interaction_terms = pd.DataFrame(df_interaction_terms, columns=['feature1', 'feature2', 'interaction'])
logging.info(df_interaction_terms.head())

# Test polynomial_features transformation
logging.info("Testing polynomial_features transformation")
df_polynomial_features = Transformation.polynomial_features(df[['feature1', 'feature2']].copy(), degree=2)
df_polynomial_features = pd.DataFrame(df_polynomial_features, columns=['feature1', 'feature2', 'feature1^2', 'feature1*feature2', 'feature2^2'])
logging.info(df_polynomial_features.head())
