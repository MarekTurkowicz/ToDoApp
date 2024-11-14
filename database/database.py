from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

engine = create_engine('sqlite:///todo_app.db')
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def initialize_database():
    """Initializes the database. Create tables if they do not exist."""
    Base.metadata.create_all(bind = engine)
