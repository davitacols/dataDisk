# tests/test_error_handling.py
import unittest
from dataflow import DataPipeline, Transformation, Validator, ParallelProcessor


def double(x):
    return x * 2


def raise_error(x):
    raise ValueError("An intentional error occurred.")


def is_even(x):
    return x if x % 2 == 0 else None


class TestErrorHandling(unittest.TestCase):
    def test_error_handling(self):
        pipeline = DataPipeline()
        transformation = Transformation(double)
        error_task = Transformation(raise_error)
        validator = Validator(is_even)

        pipeline.add_task(transformation)
        pipeline.add_task(error_task)
        pipeline.add_task(validator)

        processor = ParallelProcessor()
        result = processor.process(pipeline, 3)

        # Adjusted expectation to include the error from the validation task
        self.assertEqual(
            result, [
                6, 'Error: An intentional error occurred.',
                'Error: Data validation failed.'
            ]
        )
