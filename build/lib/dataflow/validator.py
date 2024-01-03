# dataflow/validator.py
class Validator:
    def __init__(self, validate_func):
        self.validate_func = validate_func

    def execute(self, data):
        if self.validate_func(data):
            return data
        else:
            raise ValueError("Data validation failed.")
