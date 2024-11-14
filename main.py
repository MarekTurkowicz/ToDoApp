# tests
# from database.database import initialize_database
# from controllers.user_controller import UserController
# from controllers.task_controller import TaskController
# from datetime import datetime
#
# initialize_database()
#
# user_controller = UserController()
# task_controller = TaskController()
#
# user = user_controller.create_user("hhjhJangg","hhjhhjan12345","jahhhjnn@wp.pll")
# task = task_controller.add_task("tytuł","opis",datetime(2000, 12, 31), 1)
#
#
# user_controller.close()
# task_controller.close()


# console/gui + python main.py -c/-g
import subprocess
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Uruchamianie programu w trybie konsolowym lub graficznym.")
    parser.add_argument(
        '-c', '--console', action='store_true', help="Uruchom program w trybie konsolowym"
    )
    parser.add_argument(
        '-g', '--gui', action='store_true', help="Uruchom program w trybie graficznym"
    )
    return parser.parse_args()

def launch_mode(args):
    if args.console:
        subprocess.run(['python', 'console_app.py'], check=True)
    elif args.gui:
        subprocess.run(['python', 'gui_app.py'], check=True)
    else:
        parser = argparse.ArgumentParser(description="Uruchamianie programu w trybie konsolowym lub graficznym.")
        parser.print_help()


if __name__ == "__main__":
    args = parse_arguments()
    launch_mode(args)
