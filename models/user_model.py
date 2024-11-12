from sqlalchemy import Column, Integer, String, false
from database.database import Base
from sqlalchemy.orm import  relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=False, nullable=False)
    password = Column(String(50), unique=False,nullable=False,)
    email = Column(String(50), unique=False, nullable=False)

    tasks = relationship("Task", back_populates="user")