# tests/test_visual_builder.py
import unittest
from dataDisk.visual_builder import VisualPipelineBuilder


class TestVisualPipelineBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = VisualPipelineBuilder()

    def test_add_and_visualize_tasks(self):
        # Add tasks using drag-and-drop
        self.builder.drag_and_drop("DataIngestion")
        self.builder.drag_and_drop("DataCleaning")
        self.builder.drag_and_drop("FeatureEngineering")

        # Visualize the pipeline and check if tasks are displayed
        with self.assertLogs(level='INFO') as log:
            self.builder.visualize_pipeline()

        # Check if tasks are present in the logs
        self.assertIn("DataIngestion", log.output[0])
        self.assertIn("DataCleaning", log.output[1])
        self.assertIn("FeatureEngineering", log.output[2])

    def test_remove_task(self):
        # Add a task
        self.builder.drag_and_drop("DataIngestion")

        # Remove the task and visualize the pipeline
        self.builder.remove_task("DataIngestion")

        # Visualize the pipeline and check if the task is removed
        with self.assertLogs(level='INFO') as log:
            self.builder.visualize_pipeline()

        # Check if the task is not present in the logs
        self.assertNotIn("DataIngestion", log.output[0])

    def test_export_pipeline(self):
        # Add tasks
        self.builder.drag_and_drop("DataIngestion")
        self.builder.drag_and_drop("FeatureEngineering")

        # Export the pipeline and check if the file is created
        with self.assertLogs(level='INFO') as log:
            self.builder.export_pipeline()

        # Check if the export message is present in the logs
        self.assertIn("Pipeline exported to 'pipeline.json'", log.output[0])


if __name__ == '__main__':
    unittest.main()
