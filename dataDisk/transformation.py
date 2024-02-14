# dataDisk/transformation.py

import logging
from sklearn.preprocessing import StandardScaler, Normalizer, OneHotEncoder
from sklearn.impute import SimpleImputer


class Transformation:

    def __init__(self, func):
        self.func = func

    def execute(self, data):
        try:
            return self.func(data)
        except Exception as e:
            logging.error(f"Error during transformation: {str(e)}")
            raise

    @staticmethod
    def standardize(data):
        """Standardize features by removing the mean
        and scaling to unit variance"""
        scaler = StandardScaler()
        return scaler.fit_transform(data)

    @staticmethod
    def normalize(data):
        """Normalize features to range [0, 1]"""
        normalizer = Normalizer()
        return normalizer.fit_transform(data)

    @staticmethod
    def onehot_encode(data):
        """One-hot encode categorical features"""
        encoder = OneHotEncoder(sparse=False)
        encoder.fit(data)
        return encoder.transform(data)

    @staticmethod
    def impute_missing(data):
        """Impute missing values using median"""
        imputer = SimpleImputer(strategy='median')
        return imputer.fit_transform(data)
