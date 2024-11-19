from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Footer, Static
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen, ModalScreen
from textual.widgets import SelectionList
from container import Container as AppContainer
from datetime import datetime
from views.task_view import TaskView


class ErrorModal(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield Label(self.message, id="error_message")
            yield Button("OK", id="close_modal_button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close_modal_button":
            self.dismiss()

class AddTaskView(Screen):
    CSS_PATH = '../tcss/add_task_view.tcss'

    def __init__(self):
        super().__init__()
        self.task_controller = AppContainer.getTaskController()
        self.user_id = None

    def on_mount(self):
        """Ustawia ID zalogowanego użytkownika."""
        self.user_id = self.app.logged_in_user_id
        # Dodaj opcje do listy po załadowaniu widżetów
        self.query_one("#year_selection", SelectionList).add_options(
            [(str(y), str(y)) for y in range(2023, 2025)]
        )
        self.query_one("#month_selection", SelectionList).add_options(
            [(str(m).zfill(2), str(m).zfill(2)) for m in range(1, 13)]
        )
        self.query_one("#day_selection", SelectionList).add_options(
            [(str(d).zfill(2), str(d).zfill(2)) for d in range(1, 32)]
        )

    def compose(self) -> ComposeResult:
        yield Label(
            r"""
            _      _   _______           _    
    /\       | |    | | |__   __|         | |   
    /  \    __| |  __| |    | |  __ _  ___ | | __
   / /\ \  / _` | / _` |    | | / _` |/ __|| |/ /
/ ____ \| (_| || (_| |    | || (_| |\__ \|   < 
 /_/    \_\\__,_| \__,_|    |_| \__,_||___/|_|\_\
                                                 
                                                 
""", id="header")
        with Vertical(id="form-container"):
            yield Input(placeholder="Nazwa zadania", id="task_title_input")
            yield Input(placeholder="Opis Zadania", id="task_description_input")
            with Horizontal(id="date-container"):
                yield Label("Rok:", id="year_label")
                yield SelectionList(id="year_selection")

                yield Label("Miesiąc:", id="month_label")
                yield SelectionList(id="month_selection")

                yield Label("Dzień:", id="day_label")
                yield SelectionList(id="day_selection")

            with Horizontal(id="buttons"):
                yield Button("Dodaj Task", id="add_task_button")
                yield Button("Powrót do listy zadań", id="todo_back")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id.startswith("todo_back"):
            self.app.push_screen(TaskView())
        elif event.button.id == "add_task_button":
            self.handle_task_addition()

    def get_selected_date(self) -> datetime | None:
        """Retrieve and validate the selected date."""
        year = self.query_one("#year_selection", SelectionList).selected
        month = self.query_one("#month_selection", SelectionList).selected
        day = self.query_one("#day_selection", SelectionList).selected

        if len(year) != 1 or len(month) != 1 or len(day) != 1:
            self.app.push_screen(ErrorModal("Błędne dane - wybierz dokładnie jedną wartość dla roku, miesiąca i dnia."))
            return None

        try:
            year = int(year[0])
            month = int(month[0])
            day = int(day[0])
            return datetime(year, month, day)
        except ValueError:
            self.app.push_screen(ErrorModal("Niepoprawna data - sprawdź, czy dzień pasuje do miesiąca."))
            return None

    def handle_task_addition(self):
        """Handle the addition of a task."""
        title = self.query_one("#task_title_input", Input).value
        description = self.query_one("#task_description_input", Input).value

        if not title or not description:
            self.app.push_screen(ErrorModal("Błędne dane - podaj tytuł i opis zadania."))
            return

        due_date = self.get_selected_date()
        if not due_date:
            return

        # Dodawanie zadania przez kontroler
        result = self.task_controller.add_task(
            title=title,
            description=description,
            due_date=due_date,
            user_id=self.user_id,
        )

        # Obsługa wyniku operacji
        if result is not None:
            self.app.push_screen(ErrorModal("Wystąpił błąd podczas dodawania zadania."))
        else:
            self.app.pop_screen()
