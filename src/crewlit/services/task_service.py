from crewlit.utils import load_yaml, save_yaml, dump_yaml, format_title_key
from crewlit.models import Task

class TaskService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        data = load_yaml(self.file_path)
        return {name: Task.from_dict(name, task_data) for name, task_data in data.items()}

    def save_tasks(self):
        data = {name: task.to_dict() for name, task in self.tasks.items()}
        save_yaml(self.file_path, data)

    def get_all_tasks(self):
        return self.tasks

    def update_task(self, old_name, title, description, expected_output):
        formatted_title, new_name = format_title_key(title)
        if new_name != old_name:
            del self.tasks[old_name]
        self.tasks[new_name] = Task(name=new_name, title=formatted_title, description=description, expected_output=expected_output)
        self.save_tasks()
        return formatted_title

    def delete_task(self, name):
        task = self.tasks.pop(name)
        self.save_tasks()
        return task.title

    def create_task(self, title, description, expected_output):
        formatted_title, new_name = format_title_key(title)
        if new_name not in self.tasks:
            self.tasks[new_name] = Task(name=new_name, title=formatted_title, description=description, expected_output=expected_output)
            self.save_tasks()
            return formatted_title
        return None
    
    def get_tasks_yaml(self):
        data = {name: task.to_dict() for name, task in self.tasks.items()}
        return dump_yaml(data)