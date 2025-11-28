from typing import List, Callable, Optional, Dict, Any, Union
import logging
import time
import pandas as pd
from .data_sources import DataSource
from .data_sinks import DataSink
from .transformation import Transformation


class PipelineStep:
    """Base class for pipeline steps."""
    
    def execute(self, data: Any) -> Any:
        """
        Execute the pipeline step.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_name(self) -> str:
        """Get the name of the step."""
        return self.__class__.__name__


class DataPipeline:
    """
    A pipeline for processing data through a series of steps.
    """
    
    def __init__(self, source: Optional[DataSource] = None, sink: Optional[DataSink] = None):
        """
        Initialize the data pipeline.
        
        Args:
            source: Data source to load data from
            sink: Data sink to save processed data to
        """
        self.source = source
        self.sink = sink
        self.steps = []
        self.data = None
        self.metrics = {}
        self.error_handler = None
        
    def add_step(self, step: Union[Callable, PipelineStep, Transformation]) -> 'DataPipeline':
        """
        Add a processing step to the pipeline.
        
        Args:
            step: A callable function, PipelineStep, or Transformation
            
        Returns:
            Self for method chaining
        """
        if callable(step) or isinstance(step, (PipelineStep, Transformation)):
            self.steps.append(step)
        else:
            raise ValueError("Step must be a callable function, PipelineStep, or Transformation")
        return self
        
    def add_task(self, task: Callable) -> 'DataPipeline':
        """
        Legacy method for backward compatibility.
        
        Args:
            task: A callable function
            
        Returns:
            Self for method chaining
        """
        return self.add_step(task)
    
    def set_error_handler(self, handler: Callable) -> 'DataPipeline':
        """
        Set a custom error handler function.
        
        Args:
            handler: Function that takes (exception, step_name, data) as arguments
            
        Returns:
            Self for method chaining
        """
        self.error_handler = handler
        return self
    
    def process(self) -> Any:
        """
        Process data through the pipeline using source and sink.
        
        Returns:
            Processed data
        """
        if self.source is None:
            raise ValueError("Source must be set before processing")
        
        try:
            # Load data from source
            start_time = time.time()
            self.data = self.source.load()
            self.metrics['load_time'] = time.time() - start_time
            logging.info(f"Data loaded successfully in {self.metrics['load_time']:.2f}s")
            
            # Process the data through the pipeline
            self.data = self.run(self.data)
            
            # Save processed data to sink if provided
            if self.sink is not None:
                start_time = time.time()
                self.sink.save(self.data)
                self.metrics['save_time'] = time.time() - start_time
                logging.info(f"Data saved successfully in {self.metrics['save_time']:.2f}s")
            
            return self.data
            
        except Exception as e:
            logging.error(f"Error during pipeline execution: {str(e)}")
            if self.error_handler:
                return self.error_handler(e, "process", self.data)
            raise e
    
    def run(self, data: Any) -> Any:
        """
        Run data through the pipeline steps without source/sink.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        self.data = data
        self.metrics['steps'] = {}
        
        for i, step in enumerate(self.steps):
            step_name = f"step_{i}"
            if hasattr(step, 'get_name'):
                step_name = step.get_name()
            elif hasattr(step, '__name__'):
                step_name = step.__name__
                
            try:
                start_time = time.time()
                logging.info(f"Executing step: {step_name}")
                
                if isinstance(step, Transformation):
                    self.data = step.execute(self.data)
                elif isinstance(step, PipelineStep):
                    self.data = step.execute(self.data)
                else:
                    self.data = step(self.data)
                    
                step_time = time.time() - start_time
                self.metrics['steps'][step_name] = step_time
                logging.info(f"Step {step_name} completed in {step_time:.2f}s")
                
            except Exception as e:
                logging.error(f"Error in step {step_name}: {str(e)}")
                if self.error_handler:
                    self.data = self.error_handler(e, step_name, self.data)
                else:
                    raise e
        
        self.metrics['total_processing_time'] = sum(self.metrics['steps'].values())
        return self.data
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get execution metrics for the pipeline.
        
        Returns:
            Dictionary of metrics
        """
        return self.metrics
    
    def reset(self) -> 'DataPipeline':
        """
        Reset the pipeline state.
        
        Returns:
            Self for method chaining
        """
        self.data = None
        self.metrics = {}
        return self


# Example usage:
if __name__ == '__main__':
    from dataDisk.data_sources import CSVDataSource
    from dataDisk.data_sinks import CSVSink
    from dataDisk.transformation import Transformation
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Define source and sink
    csv_data_source = CSVDataSource('customer_churn.csv')
    csv_data_sink = CSVSink('processed_customer_churn.csv')
    
    # Create the pipeline
    pipeline = DataPipeline(source=csv_data_source, sink=csv_data_sink)
    
    # Add steps
    pipeline.add_step(Transformation.data_cleaning)
    pipeline.add_step(Transformation.normalize)
    pipeline.add_step(Transformation.label_encode)
    
    # Process the data
    processed_data = pipeline.process()
    
    # Get metrics
    metrics = pipeline.get_metrics()
    print(f"Total processing time: {metrics['total_processing_time']:.2f}s")
    print("Data processing complete.")
