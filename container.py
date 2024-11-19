from typing import Dict, Any
from repositories.user_repository import UserRepository
from repositories.task_repository import TaskRepository
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from database.database import initialize_database

class Container:
    _instance: Dict[str, Any] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            cls._instance['db_connection'] = initialize_database()
            cls._initialized = True

    @classmethod
    def get_instance(cls, key: str, creator_func):
        if not cls._initialized:
            cls.initialize()

        if key not in cls._instance:
            cls._instance[key] = creator_func()
        return cls._instance[key]

    @classmethod
    def getDbConnection(cls):
        return cls.get_instance('db_connection', lambda: initialize_database())

    @classmethod
    def getUserRepository(cls):
        return cls.get_instance('user_repository', lambda: UserRepository())

    @classmethod
    def getTaskRepository(cls):
        return cls.get_instance("task_repository", lambda: TaskRepository())

    @classmethod
    def getTaskController(cls):
        return cls.get_instance("task_controller", lambda: TaskController(cls.getTaskRepository()))

    @classmethod
    def getUserController(cls):
        return cls.get_instance("user_controller", lambda: UserController(cls.getUserRepository()))