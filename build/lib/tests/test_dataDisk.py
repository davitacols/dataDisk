# tests/test_dataflow.py
import pytest
from dataDisk import DataPipeline, Transformation, Validator, ParallelProcessor # noqa


def test_pipeline_execution_order():
    pipeline = DataPipeline()
    transformation1 = Transformation(lambda x: x * 2)
    transformation2 = Transformation(lambda x: x + 5)
    validator = Validator(lambda x: x % 2 == 0)

    pipeline.add_task(transformation1)
    pipeline.add_task(transformation2)
    pipeline.add_task(validator)

    with pytest.raises(ValueError, match="Data validation failed."):
        pipeline.process(3)
