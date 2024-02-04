# tests/test_pipeline.py
import unittest
import pytest
from dataDisk import DataPipeline, Transformation, Validator

class TestPipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        pipeline = DataPipeline()
        transformation = Transformation(lambda x: x * 2)
        validator = Validator(lambda x: x % 2 == 0)

        pipeline.add_task(transformation)
        pipeline.add_task(validator)

        result = pipeline.process(3)

        self.assertEqual(result, 6)

    def test_pipeline_with_priority(self):
        pipeline = DataPipeline()
        high_priority_transformation = Transformation(lambda x: x * 3)
        low_priority_transformation = Transformation(lambda x: x + 5)

        pipeline.add_task(high_priority_transformation, priority=2)
        pipeline.add_task(low_priority_transformation, priority=1)

        result = pipeline.process(2)

        # Update the expected result based on the transformations and priorities
        self.assertEqual(result, 11)  # Adjust this value based on your pipeline logic

    def test_pipeline_with_condition(self):
        pipeline = DataPipeline()
        transformation = Transformation(lambda x: x * 2)

        pipeline.add_task(transformation, condition=lambda x: x > 0)

        result = pipeline.process(-1)

        self.assertEqual(result, -1)

    # Add similar tests for skip conditions and retry logic...

    def test_pipeline_execution_order(self):
        pipeline = DataPipeline()
        transformation1 = Transformation(lambda x: x * 2)
        transformation2 = Transformation(lambda x: x + 5)
        validator = Validator(lambda x: x % 2 == 0)

        pipeline.add_task(transformation1)
        pipeline.add_task(transformation2)
        pipeline.add_task(validator)

        with pytest.raises(ValueError, match="Data validation failed."):
            pipeline.process(3)

if __name__ == '__main__':
    unittest.main()
