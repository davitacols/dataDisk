# tests/test_parallel_processor.py
import unittest
from dataflow import DataPipeline, Transformation, Validator, ParallelProcessor


def double(x):
    return x * 2


def square(x):
    return x ** 2


def is_even(x):
    return x if x % 2 == 0 else None


class TestParallelProcessor(unittest.TestCase):
    def test_parallel_processing_multiple_tasks(self):
        pipeline = DataPipeline()
        transformation1 = Transformation(double)
        transformation2 = Transformation(square)
        validator = Validator(is_even)

        pipeline.add_task(transformation1)
        pipeline.add_task(transformation2)
        pipeline.add_task(validator)

        processor = ParallelProcessor()
        result = processor.process(pipeline, 3)

        self.assertEqual(result, [6, 9, 'Error: Data validation failed.'])
