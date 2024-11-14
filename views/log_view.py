from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Footer, Placeholder, Button
import os

class LogView(Screen):
    CSS_PATH = '../tcss/log_view_tcss.tcss'
    def compose(self) -> ComposeResult:
        # yield Header()
        yield Placeholder("log_view")
        # yield Button("Log View")
        yield Footer()

