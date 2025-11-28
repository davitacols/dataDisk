# dataDisk/transformation.py

import logging
import numpy as np
import pandas as pd
from typing import Callable, Dict, List, Union, Optional, Any, Tuple
from sklearn.preprocessing import (
    StandardScaler, Normalizer, OneHotEncoder,
    RobustScaler, PolynomialFeatures, LabelEncoder,
    MinMaxScaler, MaxAbsScaler, PowerTransformer
)
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_regression


class TransformationError(Exception):
    """Custom exception for transformation errors."""
    pass


class Transformation:
    """
    A class for applying data transformations.
    """
    
    def __init__(self, func: Callable, name: Optional[str] = None):
        """
        Initialize a transformation with a function.
        
        Args:
            func: Function to apply as transformation
            name: Optional name for the transformation
        """
        self.func = func
        self.name = name or getattr(func, '__name__', 'unknown_transformation')
        self.metadata = {}

    def execute(self, data: Any) -> Any:
        """
        Execute the transformation function on the given data.

        Args:
            data: Input data to transform

        Returns:
            Transformed data

        Raises:
            TransformationError: If transformation fails
        """
        try:
            logging.info(f"Applying transformation: {self.name}")
            result = self.func(data)
            return result
        except Exception as e:
            error_msg = f"Error during transformation '{self.name}': {str(e)}"
            logging.error(error_msg)
            raise TransformationError(error_msg) from e
            
    def get_name(self) -> str:
        """Get the name of the transformation."""
        return self.name
        
    def set_metadata(self, key: str, value: Any) -> 'Transformation':
        """
        Set metadata for the transformation.
        
        Args:
            key: Metadata key
            value: Metadata value
            
        Returns:
            Self for method chaining
        """
        self.metadata[key] = value
        return self
        
    def get_metadata(self, key: Optional[str] = None) -> Any:
        """
        Get transformation metadata.
        
        Args:
            key: Specific metadata key to retrieve, or None for all metadata
            
        Returns:
            Metadata value or dictionary of all metadata
        """
        if key is not None:
            return self.metadata.get(key)
        return self.metadata

    @classmethod
    def chain(cls, transformations: List['Transformation']) -> 'Transformation':
        """
        Chain multiple transformations into a single transformation.
        
        Args:
            transformations: List of transformations to chain
            
        Returns:
            A new transformation that applies all transformations in sequence
        """
        def chained_transform(data):
            result = data
            for transform in transformations:
                result = transform.execute(result)
            return result
            
        names = [t.get_name() for t in transformations]
        chain_name = f"Chain({','.join(names)})"
        return cls(chained_transform, name=chain_name)

    @staticmethod
    def _handle_dataframe(data: Any, func: Callable, columns: Optional[List[str]] = None) -> Any:
        """
        Helper method to handle DataFrame transformations.
        
        Args:
            data: Input data
            func: Function to apply
            columns: Specific columns to transform, or None for all
            
        Returns:
            Transformed data
        """
        if not isinstance(data, pd.DataFrame):
            return func(data)
            
        result = data.copy()
        target_columns = columns or data.columns
        
        # Filter columns that actually exist in the DataFrame
        target_columns = [col for col in target_columns if col in data.columns]
        
        if not target_columns:
            return result
            
        result[target_columns] = func(data[target_columns])
        return result

    @staticmethod
    def standardize(data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Standardize data to have zero mean and unit variance.
        
        Args:
            data: DataFrame to transform
            columns: Specific columns to transform, or None for all numeric columns
            
        Returns:
            Standardized DataFrame
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) == 0:
                return data
                
            scaler = StandardScaler()
            data[columns] = scaler.fit_transform(data[columns])
            return data
        except Exception as e:
            logging.error(f"Error during standardize transformation: {str(e)}")
            raise

    @staticmethod
    def normalize(data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Normalize data using StandardScaler.
        
        Args:
            data: DataFrame to transform
            columns: Specific columns to transform, or None for all numeric columns
            
        Returns:
            Normalized DataFrame
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) == 0:
                return data
                
            scaler = StandardScaler()
            data[columns] = scaler.fit_transform(data[columns])
            return data
        except Exception as e:
            logging.error(f"Error during normalize transformation: {str(e)}")
            raise

    @staticmethod
    def min_max_scale(data: pd.DataFrame, columns: Optional[List[str]] = None, 
                      feature_range: Tuple[float, float] = (0, 1)) -> pd.DataFrame:
        """
        Scale data to a specific range.
        
        Args:
            data: DataFrame to transform
            columns: Specific columns to transform, or None for all numeric columns
            feature_range: Range to scale to (min, max)
            
        Returns:
            Scaled DataFrame
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) == 0:
                return data
                
            scaler = MinMaxScaler(feature_range=feature_range)
            data[columns] = scaler.fit_transform(data[columns])
            return data
        except Exception as e:
            logging.error(f"Error during min_max_scale transformation: {str(e)}")
            raise

    @staticmethod
    def label_encode(data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Encode categorical columns to numeric values.
        
        Args:
            data: DataFrame to transform
            columns: Specific columns to transform, or None for all object columns
            
        Returns:
            DataFrame with encoded categories
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['object']).columns
                
            if len(columns) == 0:
                return data
                
            for col in columns:
                encoder = LabelEncoder()
                data[col] = encoder.fit_transform(data[col])
            return data
        except Exception as e:
            logging.error(f"Error during label_encode transformation: {str(e)}")
            raise

    @staticmethod
    def onehot_encode(data: pd.DataFrame, columns: Optional[List[str]] = None, 
                      drop_original: bool = True, prefix_sep: str = '_') -> pd.DataFrame:
        """
        One-hot encode categorical columns.
        
        Args:
            data: DataFrame to transform
            columns: Specific columns to transform, or None for all object columns
            drop_original: Whether to drop the original columns
            prefix_sep: Separator between column name and category value
            
        Returns:
            DataFrame with one-hot encoded categories
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['object']).columns
                
            if len(columns) == 0:
                return data
                
            encoder = OneHotEncoder(sparse=False)
            encoded_data = encoder.fit_transform(data[columns])
            
            feature_names = encoder.get_feature_names_out(columns)
            encoded_df = pd.DataFrame(encoded_data, columns=feature_names, index=data.index)
            
            if drop_original:
                data = data.drop(columns, axis=1)
                
            return pd.concat([data, encoded_df], axis=1)
        except Exception as e:
            logging.error(f"Error during onehot_encode transformation: {str(e)}")
            raise

    @staticmethod
    def data_cleaning(data: pd.DataFrame) -> pd.DataFrame:
        """
        Perform comprehensive data cleaning.
        
        Args:
            data: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        try:
            data = data.copy()
            
            # Convert columns to appropriate types
            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
            data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
            
            # Fill missing values for numeric data
            data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
            
            # Handle categorical data
            categorical_columns = data.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                # Fill missing values with most frequent value
                most_frequent = data[col].mode()[0] if not data[col].mode().empty else "unknown"
                data[col] = data[col].fillna(most_frequent)
                
                # Encode categorical data
                encoder = LabelEncoder()
                data[col] = encoder.fit_transform(data[col])
            
            return data
        except Exception as e:
            logging.error(f"Error during data_cleaning transformation: {str(e)}")
            raise

    @staticmethod
    def impute_missing(data: pd.DataFrame, strategy: str = 'mean', 
                       columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Impute missing values in the data.
        
        Args:
            data: DataFrame with missing values
            strategy: Imputation strategy ('mean', 'median', 'most_frequent', 'constant', 'knn')
            columns: Specific columns to impute, or None for all columns with missing values
            
        Returns:
            DataFrame with imputed values
        """
        try:
            data = data.copy()
            
            if columns is None:
                columns = data.columns[data.isna().any()].tolist()
                
            if len(columns) == 0:
                return data
                
            if strategy == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                data[columns] = imputer.fit_transform(data[columns])
            else:
                imputer = SimpleImputer(strategy=strategy)
                data[columns] = imputer.fit_transform(data[columns])
                
            return data
        except Exception as e:
            logging.error(f"Error during impute_missing transformation: {str(e)}")
            raise

    @staticmethod
    def log_transform(data: Union[pd.DataFrame, np.ndarray], 
                      columns: Optional[List[str]] = None) -> Union[pd.DataFrame, np.ndarray]:
        """
        Perform log transformation on numerical data.
        
        Args:
            data: Data to transform
            columns: Specific columns to transform if data is a DataFrame
            
        Returns:
            Log-transformed data
        """
        try:
            def transform_func(x):
                return np.log1p(x)
                
            return Transformation._handle_dataframe(data, transform_func, columns)
        except Exception as e:
            logging.error(f"Error during log_transform: {str(e)}")
            raise

    @staticmethod
    def sqrt_transform(data: Union[pd.DataFrame, np.ndarray], 
                       columns: Optional[List[str]] = None) -> Union[pd.DataFrame, np.ndarray]:
        """
        Perform square root transformation on numerical data.
        
        Args:
            data: Data to transform
            columns: Specific columns to transform if data is a DataFrame
            
        Returns:
            Square root-transformed data
        """
        try:
            def transform_func(x):
                x_copy = x.copy() if hasattr(x, 'copy') else x
                if isinstance(x_copy, pd.DataFrame):
                    x_copy = x_copy.fillna(0)
                else:
                    x_copy = np.nan_to_num(x_copy, nan=0.0)
                return np.sqrt(x_copy)
                
            return Transformation._handle_dataframe(data, transform_func, columns)
        except Exception as e:
            logging.error(f"Error during sqrt_transform: {str(e)}")
            raise

    @staticmethod
    def robust_scale(data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Perform robust scaling on numerical data.
        
        Args:
            data: DataFrame to scale
            columns: Specific columns to scale, or None for all numeric columns
            
        Returns:
            Robustly scaled DataFrame
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) == 0:
                return data
                
            # First impute missing values
            imputer = SimpleImputer(strategy='median')
            data[columns] = imputer.fit_transform(data[columns])
            
            # Then apply robust scaling
            scaler = RobustScaler()
            data[columns] = scaler.fit_transform(data[columns])
            
            return data
        except Exception as e:
            logging.error(f"Error during robust_scale transformation: {str(e)}")
            raise

    @staticmethod
    def binning(data: Union[pd.Series, np.ndarray], num_bins: int = 5, 
                labels: Optional[List[str]] = None) -> Union[pd.Series, np.ndarray]:
        """
        Perform binning on numerical data.
        
        Args:
            data: Data to bin
            num_bins: Number of bins to create
            labels: Optional labels for the bins
            
        Returns:
            Binned data
        """
        try:
            if isinstance(data, pd.Series):
                return pd.cut(data, bins=num_bins, labels=labels)
            else:
                data = np.array(data)
                bins = np.linspace(np.nanmin(data), np.nanmax(data), num_bins + 1)
                return np.digitize(data, bins)
        except Exception as e:
            logging.error(f"Error during binning transformation: {str(e)}")
            raise

    @staticmethod
    def interaction_terms(data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Generate interaction terms for numerical data.
        
        Args:
            data: DataFrame to transform
            columns: Specific columns to use, or None for all numeric columns
            
        Returns:
            DataFrame with interaction terms
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) < 2:
                return data
                
            # Impute missing values
            imputer = SimpleImputer(strategy='median')
            interaction_data = imputer.fit_transform(data[columns])
            
            # Generate interaction terms
            poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
            interaction_terms = poly.fit_transform(interaction_data)
            
            # Create feature names for interaction terms
            feature_names = poly.get_feature_names_out(columns)
            
            # Keep only the interaction terms (not the original features)
            interaction_df = pd.DataFrame(
                interaction_terms[:, len(columns):], 
                columns=feature_names[len(columns):],
                index=data.index
            )
            
            # Concatenate with original data
            return pd.concat([data, interaction_df], axis=1)
        except Exception as e:
            logging.error(f"Error during interaction_terms transformation: {str(e)}")
            raise

    @staticmethod
    def polynomial_features(data: pd.DataFrame, degree: int = 2, 
                           columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Generate polynomial features for numerical data.
        
        Args:
            data: DataFrame to transform
            degree: Degree of the polynomial features
            columns: Specific columns to use, or None for all numeric columns
            
        Returns:
            DataFrame with polynomial features
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) == 0:
                return data
                
            # Handle missing values
            imputer = SimpleImputer(strategy='median')
            poly_data = imputer.fit_transform(data[columns])
            
            # Generate polynomial features
            poly = PolynomialFeatures(degree=degree, include_bias=False)
            poly_features = poly.fit_transform(poly_data)
            
            # Create feature names
            feature_names = poly.get_feature_names_out(columns)
            
            # Create DataFrame with polynomial features
            poly_df = pd.DataFrame(
                poly_features, 
                columns=feature_names,
                index=data.index
            )
            
            # Drop original columns to avoid duplication
            result = data.drop(columns, axis=1)
            
            # Concatenate with polynomial features
            return pd.concat([result, poly_df], axis=1)
        except Exception as e:
            logging.error(f"Error during polynomial_features transformation: {str(e)}")
            raise
            
    @staticmethod
    def pca_transform(data: pd.DataFrame, n_components: Optional[int] = None, 
                     variance_threshold: float = 0.95) -> pd.DataFrame:
        """
        Apply PCA dimensionality reduction.
        
        Args:
            data: DataFrame to transform
            n_components: Number of components to keep, or None to use variance threshold
            variance_threshold: Minimum explained variance to retain if n_components is None
            
        Returns:
            DataFrame with PCA components
        """
        try:
            # Handle missing values
            imputer = SimpleImputer(strategy='median')
            imputed_data = imputer.fit_transform(data)
            
            # Determine number of components
            if n_components is None:
                pca = PCA(n_components=variance_threshold, svd_solver='full')
            else:
                pca = PCA(n_components=n_components)
                
            # Apply PCA
            transformed_data = pca.fit_transform(imputed_data)
            
            # Create component names
            component_names = [f"PC{i+1}" for i in range(transformed_data.shape[1])]
            
            # Create DataFrame with PCA components
            pca_df = pd.DataFrame(
                transformed_data,
                columns=component_names,
                index=data.index
            )
            
            # Add explained variance as metadata
            explained_variance = pca.explained_variance_ratio_
            
            return pca_df
        except Exception as e:
            logging.error(f"Error during pca_transform: {str(e)}")
            raise
            
    @staticmethod
    def feature_selection(data: pd.DataFrame, target: pd.Series, 
                         k: int = 10) -> pd.DataFrame:
        """
        Select top k features based on correlation with target.
        
        Args:
            data: DataFrame with features
            target: Target variable
            k: Number of features to select
            
        Returns:
            DataFrame with selected features
        """
        try:
            # Ensure k is not larger than the number of features
            k = min(k, data.shape[1])
            
            # Handle missing values
            imputer = SimpleImputer(strategy='median')
            imputed_data = imputer.fit_transform(data)
            
            # Select features
            selector = SelectKBest(f_regression, k=k)
            selected_data = selector.fit_transform(imputed_data, target)
            
            # Get selected feature names
            selected_indices = selector.get_support(indices=True)
            selected_features = data.columns[selected_indices]
            
            # Create DataFrame with selected features
            return pd.DataFrame(
                selected_data,
                columns=selected_features,
                index=data.index
            )
        except Exception as e:
            logging.error(f"Error during feature_selection: {str(e)}")
            raise
            
    @staticmethod
    def power_transform(data: pd.DataFrame, method: str = 'yeo-johnson',
                       columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Apply power transform to make data more Gaussian-like.
        
        Args:
            data: DataFrame to transform
            method: Transformation method ('yeo-johnson' or 'box-cox')
            columns: Specific columns to transform, or None for all numeric columns
            
        Returns:
            Transformed DataFrame
        """
        try:
            data = data.copy()
            if columns is None:
                columns = data.select_dtypes(include=['float64', 'int64']).columns
                
            if len(columns) == 0:
                return data
                
            # Handle missing values
            imputer = SimpleImputer(strategy='median')
            data[columns] = imputer.fit_transform(data[columns])
            
            # Apply power transform
            pt = PowerTransformer(method=method)
            data[columns] = pt.fit_transform(data[columns])
            
            return data
        except Exception as e:
            logging.error(f"Error during power_transform: {str(e)}")
            raise
