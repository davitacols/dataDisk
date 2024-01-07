# dataDisk/transformation.py
class Transformation:
    def __init__(self, func):
        self.func = func

    def execute(self, data):
        return self.func(data)
