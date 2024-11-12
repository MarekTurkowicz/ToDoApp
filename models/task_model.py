from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=True)
    due_date = Column(DateTime, nullable=True,unique=False)
    is_completed = Column(Boolean, unique=False, nullable=True, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='tasks')
