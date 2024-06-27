# tests/test_data_pipeline.py
import unittest
from dataDisk import DataPipeline, Transformation, Validator


class TestDataPipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        pipeline = DataPipeline()
        transformation = Transformation(lambda x: x * 2)
        validator = Validator(lambda x: x % 2 == 0)

        pipeline.add_task(transformation)
        pipeline.add_task(validator)

        # Check intermediate result after the transformation
        intermediate_result = pipeline.process(3)
        self.assertEqual(intermediate_result, 6)

        # Check the final result after the entire pipeline
        result = pipeline.process(3)
        self.assertEqual(result, 6)
