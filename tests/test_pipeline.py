import unittest
import pandas as pd
import os
from dataDisk.pipeline import DataPipeline
from dataDisk.data_sources import CSVDataSource
from dataDisk.data_sinks import CSVSink
from dataDisk.transformation import Transformation


class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        # Create a sample CSV file for testing
        self.sample_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [6, 7, 8, 9, 10],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'feature3': [None, 2.0, None, 4.0, 5.0]
        })
        self.sample_data.to_csv('test_input.csv', index=False)
        
        # Output file path
        self.output_path = 'test_output.csv'
        
        # Initialize DataPipeline components
        self.source = CSVDataSource('test_input.csv')
        self.sink = CSVSink(self.output_path)
        self.pipeline = DataPipeline(source=self.source, sink=self.sink)
        
        # Add tasks to the pipeline
        self.pipeline.add_task(Transformation.data_cleaning)
        self.pipeline.add_task(Transformation.normalize)
        self.pipeline.add_task(Transformation.label_encode)

    def tearDown(self):
        # Clean up the files created during tests
        if os.path.exists('test_input.csv'):
            os.remove('test_input.csv')
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_pipeline_process(self):
        # Process the data through the pipeline
        processed_data = self.pipeline.process()
        
        # Check if the output file is created
        self.assertTrue(os.path.exists(self.output_path))
        
        # Load the processed data
        output_data = pd.read_csv(self.output_path)
        
        # Check if the processed data has the expected transformations
        self.assertEqual(processed_data.shape, output_data.shape)
        self.assertNotIn('category', output_data.columns)
        self.assertIn('feature1', output_data.columns)
        self.assertIn('feature2', output_data.columns)
        self.assertIn('feature3', output_data.columns)
        
        # Verify data cleaning and normalization
        self.assertAlmostEqual(processed_data['feature3'][0], processed_data['feature3'].mean(), places=1)
        self.assertAlmostEqual(processed_data['feature2'][0], -1.264911, places=1)

if __name__ == '__main__':
    unittest.main()
