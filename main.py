from database.database import initialize_database
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from datetime import datetime

initialize_database()

user_controller = UserController()
task_controller = TaskController()

user = user_controller.create_user("hhjhJangg","hhjhhjan12345","jahhhjnn@wp.pll")
task = task_controller.add_task("tytuł","opis",datetime(2000, 12, 31), 1)


user_controller.close()
task_controller.close()