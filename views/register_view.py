from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Footer
from textual.containers import Container
from textual.screen import Screen, ModalScreen
from container import Container as AppContainer  # Import singletona Container
from views.task_view import TaskView


class ErrorModal(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield Label(self.message, id="error_message")  # Wyświetlany komunikat
            yield Button("OK", id="close_modal_button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close_modal_button":
            self.dismiss()


class RegisterView(Screen):
    CSS_PATH = '../tcss/log_view_tcss.tcss'

    def __init__(self):
        super().__init__()
        # Pobieramy kontrolery z Container
        self.user_controller = AppContainer.getUserController()
        self.task_controller = AppContainer.getTaskController()

    def compose(self) -> ComposeResult:
        """Budowanie widoku rejestracji."""
        yield Label("Rejestracja", id="header")
        yield Input(placeholder="Enter your username", id="username_input")
        yield Input(placeholder="Enter your password", id="password_input", password=True)
        yield Input(placeholder="Enter your email", id="email_input")
        yield Button("Create User", id="create_user_button")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Obsługa przycisku 'Create User'."""
        if event.button.id == "create_user_button":
            # Pobieramy dane z pól tekstowych
            username = self.query_one("#username_input", Input).value
            password = self.query_one("#password_input", Input).value
            email = self.query_one("#email_input", Input).value

            # Walidacja: upewnij się, że wszystkie pola są wypełnione
            if not all([username, password, email]):
                self.app.bell()  # Powiadomienie o błędzie (np. pustych polach)
                return

            # Tworzymy użytkownika za pomocą kontrolera
            result = self.user_controller.create_user(
                user=username,
                password=password,
                email=email,
            )

            # Informujemy o wyniku operacji
            if result:
                self.app.push_screen(TaskView())
            else:

                self.app.push_screen(ErrorModal("Błędne dane. Spróbuj ponownie."))
