# dataDisk/visual_builder.py
import json


class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class VisualPipelineBuilder:
    def __init__(self):
        self.tasks = []

    def drag_and_drop(self, task_name):
        # For simplicity, assume tasks are predefined,
        # and users can only add them.
        predefined_tasks = {
            "DataIngestion": "Ingest raw data from sources.",
            "DataCleaning": "Clean and preprocess data.",
            "FeatureEngineering": "Create new features."
        }

        if task_name in predefined_tasks:
            task = Task(task_name, predefined_tasks[task_name])
            self.tasks.append(task)
            print(f"Task '{task.name}' added to the pipeline.")
        else:
            print(f"Invalid task: {task_name}. Task not added.")

    def remove_task(self, task_name):
        # Remove a task by name
        self.tasks = [task for task in self.tasks if task.name != task_name]
        print(f"Task '{task_name}' removed from the pipeline.")

    def visualize_pipeline(self):
        if not self.tasks:
            print("Pipeline is empty.")
        else:
            print("Visualizing Pipeline:")
            for task in self.tasks:
                print(f"- {task.name}: {task.description}")

    def export_pipeline(self):
        # Export the pipeline to a JSON file
        data = [
            {
                "name": task.name, "description": task.description
            } for task in self.tasks
        ]
        with open("pipeline.json", "w") as file:
            json.dump(data, file)
            print("Pipeline exported to 'pipeline.json'.")
