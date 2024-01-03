# tests/test_pipeline.py
import unittest
from dataflow import DataPipeline, Transformation, Validator


class TestPipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        pipeline = DataPipeline()
        transformation = Transformation(lambda x: x * 2)
        validator = Validator(lambda x: x % 2 == 0)

        pipeline.add_task(transformation)
        pipeline.add_task(validator)

        result = pipeline.process(3)

        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()
