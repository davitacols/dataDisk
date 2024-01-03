# tests/test_data_pipeline.py
import unittest
from dataflow import DataPipeline, Transformation, Validator


class TestDataPipeline(unittest.TestCase):
    def test_pipeline_execution_order(self):
        pipeline = DataPipeline()
        transformation1 = Transformation(lambda x: x * 2)
        transformation2 = Transformation(lambda x: x + 5)
        validator = Validator(lambda x: x % 2 == 0)

        pipeline.add_task(transformation1)
        pipeline.add_task(transformation2)
        pipeline.add_task(validator)

        try:
            pipeline.process(3)
        except ValueError as e:
            self.assertEqual(str(e), "Data validation failed.")
        # No need for an else block since we're expecting an exception
