from database.database import SessionLocal
from models.task_model import Task
from datetime import datetime
from typing import Optional, List

class TaskRepository:
    def __init__(self):
        self.session = SessionLocal()

    def add_task(self, title: str, description: str, due_date: Optional[datetime], user_id: int) -> Task:
        new_task = Task(title=title, description=description, due_date=due_date, is_completed=False, user_id=user_id)
        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        return new_task

    def get_tasks_by_user_id(self, id: int) -> List[Task]:
        return self.session.query(Task).filter(Task.user_id == id).all()

    def get_tasks_by_title(self, title: str) -> List[Task]:
        return self.session.query(Task).filter(Task.title == title).all()

    def get_task_by_due_date(self, due_date: datetime) -> List[Task]:
        return self.session.query(Task).filter(Task.due_date == due_date).all()

    def get_tasks_done(self, user_id: int) -> List[Task]:
        return self.session.query(Task).filter(
            Task.user_id == user_id,
            Task.is_completed == True
        ).all()

    def get_task_by_id(self, task_id: int) -> List[Task]:
        return self.session.query(Task).filter(Task.id == task_id).first()

    def mark_task_completed(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.is_completed = True
            self.session.commit()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()
