from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Footer
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen, ModalScreen
from container import Container as AppContainer  # Import singletona Container
from views.register_view import RegisterView


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


class LogView(Screen):
    CSS_PATH = '../tcss/log_view_tcss.tcss'

    def __init__(self):
        super().__init__()
        # Kontrolery będą dynamicznie pobierane z Container
        self.user_controller = AppContainer.getUserController()
        self.task_controller = AppContainer.getTaskController()

    def compose(self) -> ComposeResult:
        with Container(classes="header"):
            yield Label("""
  _       ____    _____   _____  _   _  
 | |     / __ \  / ____| |_   _|| \ | | 
 | |    | |  | || |  __    | |  |  \| | 
 | |    | |  | || | |_ |   | |  | . ` | 
 | |____| |__| || |__| |  _| |_ | |\  | 
 |______|\____/  \_____| |_____||_| \_| 
                                        
                                        
""", id="header")
        with Container(classes="t2"):
            yield Input(placeholder="Enter your username", id="username_input")
            yield Input(placeholder="Enter your password", id="password_input", password=True)
            with Horizontal(classes="buttons"):
                yield Button("Zaloguj się", id="login_button")
                yield Button("Zarejestruj sie", id="register_button")
        yield Footer()  # Stopka

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "register_button":
            self.app.push_screen(RegisterView())

        if event.button.id == "login_button":
            # Pobieramy dane z pól tekstowych
            username = self.query_one("#username_input", Input).value
            password = self.query_one("#password_input", Input).value

            # Sprawdzamy użytkownika w bazie danych
            user_checked = self.user_controller.get_user_by_username_and_password(username, password)
            if user_checked is None:
                # Wyświetlamy modal z błędem
                self.app.push_screen(ErrorModal("Błędny login lub hasło. Spróbuj ponownie."))
            else:
                # Zapisujemy dane użytkownika w aplikacji
                self.app.set_logged_in_user_username(user_checked.username)
                self.app.set_logged_in_user_id(user_checked.id)

                # Przechodzimy do TaskView
                from views.task_view import TaskView
                self.app.push_screen(TaskView())

    async def on_mount(self) -> None:
        """Działania po załadowaniu widoku."""
        self.refresh()
