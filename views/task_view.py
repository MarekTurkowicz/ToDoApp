from textual.app import ComposeResult
from textual.containers import Container, ScrollableContainer, Vertical, Horizontal
from textual.widgets import Label, Button, Footer
from textual.screen import Screen
from container import Container as AppContainer
from datetime import datetime


class TaskView(Screen):
    CSS_PATH = "../tcss/task_view_tcss.tcss"

    def __init__(self):
        super().__init__()
        self.user_controller = AppContainer.getUserController()
        self.task_controller = AppContainer.getTaskController()
        self.username = self.app.logged_in_user
        self.user_id = self.app.logged_in_user_id

    def on_mount(self):
        """Initialize user info and tasks after the screen is mounted."""
        self.refresh_tasks()

    def compose(self) -> ComposeResult:
        """Create the layout of the task view."""
        # Header Section
        with Vertical(classes="header-container"):
            yield Label("""
  _______  ____    _____    ____              _____   _____  
 |__   __|/ __ \  |  __ \  / __ \      /\    |  __ \ |  __ \ 
    | |  | |  | | | |  | || |  | |    /  \   | |__) || |__) |
    | |  | |  | | | |  | || |  | |   / /\ \  |  ___/ |  ___/ 
    | |  | |__| | | |__| || |__| |  / ____ \ | |     | |     
    |_|   \____/  |_____/  \____/  /_/    \_\|_|     |_|     
                                                             
                                                             
""", id="app-title")
        with Vertical(classes="header2-container"):
            with Horizontal():
                yield Button("Dodaj Task", id="add_task_button")
                yield Label(f"        Zalogowany jako: {self.username or 'Nieznany'}    |    DZIŚ: {datetime.now().strftime('%d.%m.%Y')}", id="user_date_info")

        # Tasks Section
        with Vertical(classes="tasks-section"):
            yield Label("Zadania:", id="tasks-title")
            with ScrollableContainer(id="tasks_scrollable"):
                pass

            yield Label("Zadania ukończone:", id="completed-tasks-title")
            with ScrollableContainer(id="completed_tasks_scrollable"):
                pass

        # Footer Section
        with Horizontal(classes="footer-container"):
            yield Button("Wyloguj się", id="logout_button")
            yield Button("Powrót do logowania", id="return_to_login_button")

        yield Footer()

    def refresh_tasks(self):
        tasks_scrollable = self.query_one("#tasks_scrollable", ScrollableContainer)
        completed_tasks_scrollable = self.query_one("#completed_tasks_scrollable", ScrollableContainer)

        tasks_scrollable.remove_children()
        completed_tasks_scrollable.remove_children()

        if not self.user_id:
            tasks_scrollable.mount(Label("Błąd: Brak ID użytkownika.", id="error_message"))
            return

        tasks = self.task_controller.get_tasks_by_user_id(self.user_id)
        if tasks:
            for task in tasks:
                tasks_scrollable.mount(Label(f"- {task.title}: {task.description}", classes="task-item"))
        else:
            tasks_scrollable.mount(Label("Brak zadań do wykonania.", id="no_tasks_message"))

        # Pobierz ukończone zadania użytkownika
        completed_tasks = self.task_controller.get_tasks_done(self.user_id)
        if completed_tasks:
            for task in completed_tasks:
                completed_tasks_scrollable.mount(
                    Label(f"- {task.title}: {task.description}", classes="completed-task-item"))
        else:
            completed_tasks_scrollable.mount(Label("Brak ukończonych zadań.", id="no_completed_tasks_message"))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button events."""
        if event.button.id == "add_task_button":
            from views.add_task_view import AddTaskView
            self.app.push_screen(AddTaskView())
        elif event.button.id.startswith("done_task_"):
            # Mark the task as completed
            task_id = int(event.button.id.split("_")[-1])
            self.task_controller.mark_task_completed(task_id)
            self.refresh_tasks()
        elif event.button.id == "logout_button":
            self.app.logged_in_user = None
            self.app.logged_in_user_id = None
            from views.log_view import LogView
            self.app.push_screen(LogView())
        elif event.button.id == "return_to_login_button":
            from views.log_view import LogView
            self.app.push_screen(LogView())
