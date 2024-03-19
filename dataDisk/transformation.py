import logging
import numpy as np
from sklearn.preprocessing import StandardScaler, Normalizer, OneHotEncoder
from sklearn.impute import SimpleImputer


class Transformation:

    def __init__(self, func):
        """
        Initializes a Transformation object with a specific function.

        Args:
            func (callable): The transformation function to be applied.
        """
        self.func = func

    def execute(self, data):
        """
        Executes the stored transformation function on the provided data.

        Args:
            data (numpy.ndarray): The data to be transformed.

        Returns:
            numpy.ndarray: The transformed data.

        Raises:
            Exception: Any exception raised during transformation.
        """
        try:
            logging.info(f"Applying transformation: {self.func.__name__}")
            return self.func(data)
        except Exception as e:
            logging.error(f"Error during transformation: {str(e)}")
            raise

    @staticmethod
    def standardize(data):
        """
        Standardizes features by removing the mean and scaling to unit variance.

        Args:
            data (numpy.ndarray): The data to be standardized.

        Returns:
            numpy.ndarray: The standardized data.
        """
        scaler = StandardScaler()
        return scaler.fit_transform(data)

    @staticmethod
    def normalize(data):
        """
        Normalizes features to range [0, 1].

        Args:
            data (numpy.ndarray): The data to be normalized.

        Returns:
            numpy.ndarray: The normalized data.
        """
        normalizer = Normalizer()
        return normalizer.fit_transform(data)

    @staticmethod
    def onehot_encode(data):
        """
        One-hot encodes categorical features.

        Args:
            data (numpy.ndarray): The data to be one-hot encoded.

        Returns:
            numpy.ndarray: The one-hot encoded data.
        """
        data = np.array(data)  # Convert input data to a NumPy array
        encoder = OneHotEncoder()
        encoder.fit(data)
        return encoder.transform(data).toarray()  # Convert sparse matrix to a dense NumPy array

    @staticmethod
    def impute_missing(data):
        """
        Imputes missing values using the median strategy.

        Args:
            data (numpy.ndarray): The data with missing values.

        Returns:
            numpy.ndarray: The data with imputed missing values.
        """
        imputer = SimpleImputer(strategy='median')
        return imputer.fit_transform(data)