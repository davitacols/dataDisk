import unittest
from unittest.mock import MagicMock, patch
from dataDisk.pipeline import DataPipeline


class MockTask:
    def __init__(self, name, should_fail=False):
        self.name = name
        self.should_fail = should_fail

    def execute(self, data):
        if self.should_fail:
            raise Exception(f"Task {self.name} failed")
        return f"{data} processed by {self.name}"


class TestDataPipeline(unittest.TestCase):

    def test_process_with_source_and_sink(self):
        # Mock source and sink
        mock_source = MagicMock()
        mock_sink = MagicMock()

        # Mock data read and write
        mock_source.read.return_value = "input_data"
        mock_sink.write = MagicMock()

        # Initialize pipeline with source and sink
        pipeline = DataPipeline(source=mock_source, sink=mock_sink)

        # Add tasks to the pipeline
        task1 = MockTask("task1")
        task2 = MockTask("task2")
        pipeline.add_task(task1)
        pipeline.add_task(task2)

        # Process the data
        result = pipeline.process()

        # Check if the source's read method was called
        mock_source.read.assert_called_once()

        # Check if the tasks were executed in order
        self.assertEqual(result, "input_data processed by task1 processed by task2")

        # Check if the sink's write method was called with the correct data
        mock_sink.write.assert_called_once_with(result)

    def test_process_with_input_data(self):
        # Mock sink
        mock_sink = MagicMock()

        # Mock data write
        mock_sink.write = MagicMock()

        # Initialize pipeline with sink
        pipeline = DataPipeline(sink=mock_sink)

        # Add tasks to the pipeline
        task1 = MockTask("task1")
        task2 = MockTask("task2")
        pipeline.add_task(task1)
        pipeline.add_task(task2)

        # Process the data
        result = pipeline.process(input_data="input_data")

        # Check if the tasks were executed in order
        self.assertEqual(result, "input_data processed by task1 processed by task2")

        # Check if the sink's write method was called with the correct data
        mock_sink.write.assert_called_once_with(result)

    def test_process_with_task_failure(self):
        # Mock source and sink
        mock_source = MagicMock()
        mock_sink = MagicMock()

        # Mock data read and write
        mock_source.read.return_value = "input_data"

        # Initialize pipeline with source and sink
        pipeline = DataPipeline(source=mock_source, sink=mock_sink)

        # Add tasks to the pipeline
        task1 = MockTask("task1")
        task2 = MockTask("task2", should_fail=True)
        pipeline.add_task(task1)
        pipeline.add_task(task2)

        # Process the data and check for exception
        with self.assertRaises(ValueError) as context:
            pipeline.process()

        self.assertIn("Error during pipeline execution: Task task2 failed", str(context.exception))

        # Check if the source's read method was called
        mock_source.read.assert_called_once()

        # Check if the sink's write method was not called
        mock_sink.write.assert_not_called()

    def test_add_task(self):
        pipeline = DataPipeline()
        task = MockTask("task1")
        pipeline.add_task(task)
        self.assertEqual(len(pipeline.tasks), 1)
        self.assertEqual(pipeline.tasks[0], task)


if __name__ == '__main__':
    unittest.main()
