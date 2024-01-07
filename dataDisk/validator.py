# dataDisk/validator.py
import logging


class Validator:
    def __init__(self, validate_func):
        self.validate_func = validate_func

    def execute(self, data):
        try:
            if self.validate_func(data):
                return data
            else:
                raise ValueError("Data validation failed.")
        except Exception as e:
            logging.error(f"Error during validation: {str(e)}")
            raise  # Re-raise the exception after logging
