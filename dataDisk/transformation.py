import logging
import numpy as np
from sklearn.preprocessing import StandardScaler, Normalizer, OneHotEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer


class Transformation:
    def __init__(self, func):
        """ Initializes a Transformation object with a specific function.
        Args:
            func (callable): The transformation function to be applied.
        """
        self.func = func

    def execute(self, data):
        try:
            logging.info(f"Applying transformation: {self.func.__name__}")
            return self.func(data)
        except Exception as e:
            logging.error(f"Error during transformation: {str(e)}")
            raise

    @staticmethod
    def standardize(data):
        # Handle missing values
        imputer = SimpleImputer(strategy='median')
        data = imputer.fit_transform(data)

        scaler = StandardScaler()
        return scaler.fit_transform(data)

    @staticmethod
    def normalize(data):
        # Handle missing values
        imputer = SimpleImputer(strategy='median')
        data = imputer.fit_transform(data)

        normalizer = Normalizer()
        return normalizer.fit_transform(data)

    @staticmethod
    def onehot_encode(data):
        encoder = OneHotEncoder()
        encoder.fit(data)
        return encoder.transform(data).toarray()

    @staticmethod
    def impute_missing(data):
        imputer = SimpleImputer(strategy='median')
        return imputer.fit_transform(data)

    @staticmethod
    def log_transform(data):
        return np.log1p(data)

    @staticmethod
    def sqrt_transform(data):
        # Handle NaN values by replacing them with zero
        data = np.nan_to_num(data, nan=0.0)
        return np.sqrt(data)



    @staticmethod
    def robust_scale(data):
        # Handle missing values
        imputer = SimpleImputer(strategy='median')
        data_imputed = imputer.fit_transform(data)

        scaler = RobustScaler()
        scaled_data = scaler.fit_transform(data_imputed)

        # Reinsert NaN values to maintain the original data structure
        scaled_data_with_nan = np.where(np.isnan(data), np.nan, scaled_data)

        return scaled_data_with_nan
