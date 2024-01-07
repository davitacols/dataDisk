# dataDisk/pipeline.py


class DataPipeline:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def process(self, input_data):
        try:
            for task in self.tasks:
                input_data = task.execute(input_data)
            return input_data
        except Exception as e:
            raise ValueError(f"Error during pipeline execution: {str(e)}")
