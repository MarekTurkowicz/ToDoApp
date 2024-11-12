from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

engine = create_engine('sqlite:///todo_app.db') #tworzenie silnika db
Base = declarative_base() #bazowa klasa dla modeli sqlalchemy

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) #konfig sesji

def initialize_database():
    """Initializes the database. Create tables if they do not exist."""
    Base.metadata.create_all(bind = engine) #na bazie istniejących modeli