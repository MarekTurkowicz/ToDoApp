from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder

class RegisterView(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("register")
        yield Footer()


        