from datetime import datetime
from repositories.task_repository import TaskRepository

class TaskController:
    def __init__(self, task_repository):
        self.repository = task_repository

    def add_task(self, title, description, due_date, user_id: int):
        self.repository.add_task(title, description, due_date, user_id)

    def get_tasks_by_user_id(self, user_id: int):
        return self.repository.get_tasks_by_user_id(user_id)

    def get_task_by_title(self, title: str):
        self.repository.get_tasks_by_id(title)

    def get_tasks_done(self, user_id: int):
        return self.repository.get_tasks_done(user_id)

    def mark_task_completed(self, id: int):
        self.repository.mark_task_completed(id)

    def delete_task(self, id: int):
        self.repository.delete_task(id)

    def close(self):
        self.repository.close()