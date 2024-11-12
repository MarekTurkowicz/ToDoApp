from datetime import datetime

from repositories.task_repository import TaskRepository

class TaskController:
    def __init__(self):
        self.repository = TaskRepository()

    def add_task(self, title, description, due_date, user_id: int):
        self.repository.add_task(title, description, due_date, user_id)

    def get_task_by_id(self, id: int):
        self.repository.get_tasks_by_id(id)

    def get_task_by_title(self, title: str):
        self.repository.get_tasks_by_id(title)

    def mark_task_completed(self, id: int):
        self.repository.mark_task_completed(id)

    def delete_task(self, id: int):
        self.repository.delete_task(id)

    def close(self):
        self.repository.close()