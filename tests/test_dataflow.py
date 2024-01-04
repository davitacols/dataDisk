# tests/test_dataflow.py
from dataflow import DataPipeline, Transformation, Validator, ParallelProcessor

def test_pipeline_execution_order():
    pipeline = DataPipeline()
    transformation1 = Transformation(lambda x: x * 2)
    transformation2 = Transformation(lambda x: x + 5)
    validator = Validator(lambda x: x % 2 == 0)

    pipeline.add_task(transformation1)
    pipeline.add_task(transformation2)
    pipeline.add_task(validator)

    result = pipeline.process(3)
    assert result == [14]
