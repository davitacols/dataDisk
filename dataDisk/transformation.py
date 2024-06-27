# dataDisk/transformations.py

import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    StandardScaler, Normalizer, OneHotEncoder,
    RobustScaler, PolynomialFeatures, LabelEncoder
)
from sklearn.impute import SimpleImputer
import sqlite3


class Transformation:
    def __init__(self, func):
        self.func = func

    def execute(self, data):
        """
        Execute the transformation function on the given data.

        Parameters:
        - data (DataFrame or ndarray): Input data to transform.

        Returns:
        - Transformed data after applying the transformation function.
        """
        try:
            logging.info(f"Applying transformation: {self.func.__name__}")
            return self.func(data)
        except Exception as e:
            logging.error(f"Error during transformation: {str(e)}")
            raise

    @staticmethod
    def standardize(data):
        try:
            logging.info("Data before standardization:")
            logging.info(data.head())
            scaler = StandardScaler()
            numeric_data = data.select_dtypes(include=['float64', 'int64'])
            numeric_data = scaler.fit_transform(numeric_data)

            data.loc[:, numeric_data.columns] = numeric_data
            logging.info("Data after standardization:")
            logging.info(data.head())
            return data
        except Exception as e:
            logging.error(f"Error during standardize transformation: {str(e)}")
            raise

    @staticmethod
    def normalize(data):
        logging.info("Applying transformation: normalize")
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

        logging.info(f"Numeric columns to normalize: {numeric_columns}")

        # Normalize numeric data
        scaler = StandardScaler()
        data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

        logging.info("Data after normalization:")
        logging.info(data.head())
        return data

    @staticmethod
    def label_encode(data):
        logging.info("Applying transformation: label_encode")
        categorical_columns = data.select_dtypes(include=['object']).columns

        logging.info(f"Categorical columns to encode: {categorical_columns}")

        # Encode categorical data
        label_encoder = LabelEncoder()
        for col in categorical_columns:
            data[col] = label_encoder.fit_transform(data[col])

        logging.info("Data after label encoding:")
        logging.info(data.head())
        return data

    @staticmethod
    def onehot_encode(data):
        try:
            logging.info("Data before one-hot encoding:")
            logging.info(data.head())
            categorical_data = data.select_dtypes(include=['object'])

            encoder = OneHotEncoder(sparse=False)
            encoded_data = encoder.fit_transform(categorical_data)

            encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_data.columns))
            data = data.drop(categorical_data.columns, axis=1)
            data = pd.concat([data, encoded_df], axis=1)
            logging.info("Data after one-hot encoding:")
            logging.info(data.head())
            return data
        except Exception as e:
            logging.error(f"Error during onehot_encode transformation: {str(e)}")
            raise

    @staticmethod
    def data_cleaning(data):
        logging.info("Applying transformation: data_cleaning")
        logging.info("Data before cleaning:")
        logging.info(data.head())

        # Assuming the first four columns are numeric and the last one is categorical
        numeric_data = data.iloc[:, :-1]
        categorical_data = data.iloc[:, -1]

        numeric_columns = numeric_data.columns
        categorical_columns = [categorical_data.name]

        logging.info(f"Numeric data columns: {numeric_columns}")
        logging.info(f"Categorical data columns: {categorical_columns}")

        # Fill missing values for numeric data
        numeric_data = numeric_data.fillna(numeric_data.mean())

        # Standardize numeric data
        scaler = StandardScaler()
        numeric_data = pd.DataFrame(scaler.fit_transform(numeric_data), columns=numeric_columns)

        # Encode categorical data
        label_encoder = LabelEncoder()
        categorical_data = label_encoder.fit_transform(categorical_data)
        categorical_data = pd.DataFrame(categorical_data, columns=categorical_columns)

        # Combine cleaned numeric and categorical data
        cleaned_data = pd.concat([numeric_data, categorical_data], axis=1)

        logging.info("Data after cleaning:")
        logging.info(cleaned_data.head())
        return cleaned_data

    @staticmethod
    def impute_missing(data):
        """
        Impute missing values in numerical and non-numerical columns separately.

        Parameters:
        - data (DataFrame): Input data with missing values.

        Returns:
        - Data with missing values imputed.
        """
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        numeric_imputer = SimpleImputer(strategy='median')
        data[numeric_cols] = numeric_imputer.fit_transform(data[numeric_cols])

        non_numeric_cols = data.select_dtypes(exclude=[np.number]).columns
        non_numeric_imputer = SimpleImputer(strategy='most_frequent')
        data[non_numeric_cols] = non_numeric_imputer.fit_transform(data[non_numeric_cols])

        return data

    @staticmethod
    def log_transform(data):
        """
        Perform log transformation on numerical data.

        Parameters:
        - data (ndarray or DataFrame): Input data to transform.

        Returns:
        - Log-transformed data.
        """
        return np.log1p(data)

    @staticmethod
    def sqrt_transform(data):
        """
        Perform square root transformation on numerical data, handling NaN values.

        Parameters:
        - data (ndarray or DataFrame): Input data to transform.

        Returns:
        - Square root-transformed data.
        """
        data = np.nan_to_num(data, nan=0.0)
        return np.sqrt(data)

    @staticmethod
    def robust_scale(data):
        """
        Perform robust scaling on numerical data after imputing missing values with median.

        Parameters:
        - data (ndarray or DataFrame): Input data to scale.

        Returns:
        - Robust-scaled data.
        """
        imputer = SimpleImputer(strategy='median')
        data_imputed = imputer.fit_transform(data)

        scaler = RobustScaler()
        scaled_data = scaler.fit_transform(data_imputed)

        # Convert back to DataFrame if the input was a DataFrame
        if isinstance(data, pd.DataFrame):
            scaled_data = pd.DataFrame(scaled_data, columns=data.columns)
        return scaled_data

    @staticmethod
    def binning(data, num_bins=5):
        """
        Perform binning on numerical data.

        Parameters:
        - data (ndarray or DataFrame): Input data to bin.
        - num_bins (int): Number of bins to create.

        Returns:
        - Binned data.
        """
        bins = np.linspace(np.min(data), np.max(data), num_bins)
        return np.digitize(data, bins)

    @staticmethod
    def interaction_terms(data):
        """
        Generate interaction terms for numerical data.

        Parameters:
        - data (ndarray or DataFrame): Input data to transform.

        Returns:
        - Data with interaction terms.
        """
        imputer = SimpleImputer(strategy='median')
        data_imputed = imputer.fit_transform(data)

        poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
        return poly.fit_transform(data_imputed)

    @staticmethod
    def polynomial_features(data, degree=2, nan_replacement=-1):
        """
        Generate polynomial features for numerical data.

        Parameters:
        - data (ndarray or DataFrame): Input data to transform.
        - degree (int): Degree of the polynomial features.
        - nan_replacement (int or float): Value to replace NaNs in the data.

        Returns:
        - Data with polynomial features.
        """
        data = np.nan_to_num(data, nan=nan_replacement)

        poly = PolynomialFeatures(degree=degree, include_bias=False)
        return poly.fit_transform(data)
