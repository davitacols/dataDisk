# dataDisk/transformation.py
import logging


class Transformation:
    def __init__(self, func):
        self.func = func

    def execute(self, data):
        try:
            return self.func(data)
        except Exception as e:
            logging.error(f"Error during transformation: {str(e)}")
            raise  # Re-raise the exception after logging
