# dataflow/pipeline.py
class DataPipeline:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def process(self, input_data):
        for task in self.tasks:
            input_data = task.execute(input_data)
        return input_data
