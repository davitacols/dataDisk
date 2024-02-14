# dataDisk/pipeline.py

from dataDisk.data_sources import DataSource

class DataPipeline:

    def __init__(self, source=None, sink=None): 
        self.source = source
        self.sink = sink
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def process(self, input_data=None):
        if self.source:
            input_data = self.source.read()

        try:
            for task in self.tasks:
                input_data = task.execute(input_data)

            if self.sink:
                self.sink.write(input_data)

            return input_data

        except Exception as e:
            raise ValueError(f"Error during pipeline execution: {str(e)}")
