from textual.app import App
from container import Container
from database.database import initialize_database
from views.log_view import LogView
from views.register_view import RegisterView
from views.task_view import TaskView
from views.add_task_view import AddTaskView


class ModesApp(App):
    BINDINGS = [
        ("j", "switch_mode('lv')", "LogView"),
        ("k", "switch_mode('rv')", "RegisterView"),
        ("t", "switch_mode('tv')", "TaskView"),
        ("at", "switch_mode('atv')", "AddTaskView"),
    ]
    MODES = {
        "lv": LogView,
        "rv": RegisterView,
        "tv": TaskView,
        "atv": AddTaskView,
    }

    def __init__(self):
        super().__init__()
        Container.getDbConnection()
        # Pobieramy kontrolery z Container
        self.user_controller = Container.getUserController()
        self.task_controller = Container.getTaskController()
        self.logged_in_user = None
        self.logged_in_user_id = None

    def set_logged_in_user_username(self, user):
        """Ustawia nazwę zalogowanego użytkownika."""
        self.logged_in_user = user

    def set_logged_in_user_id(self, id):
        """Ustawia ID zalogowanego użytkownika."""
        self.logged_in_user_id = id

    def action_switch_mode(self, mode: str) -> None:
        """Przełączanie między widokami."""
        if mode == "lv":
            self.push_screen(LogView())
        elif mode == "rv":
            self.push_screen(RegisterView())
        elif mode == "tv":
            self.push_screen(TaskView())
        elif mode == "atv":
            self.push_screen(AddTaskView())

    def on_mount(self) -> None:
        """Akcje po załadowaniu aplikacji."""
        self.action_switch_mode("lv")  # Domyślny widok na start

    def on_exit(self) -> None:
        """Czyszczenie zasobów po zamknięciu aplikacji."""
        self.user_controller.close()
        self.task_controller.close()


if __name__ == "__main__":
    ModesApp().run()
