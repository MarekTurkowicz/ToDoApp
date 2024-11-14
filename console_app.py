from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder

from views.log_view import LogView
from views.register_view import RegisterView

class ModesApp(App):
    BINDINGS = [
    ("j", "switch_mode('lv')", "LogView"),
    ("k", "switch_mode('rv')", "RegisterView")
    ]
    MODES = {
        "lv" : LogView,
        "rv" : RegisterView
    }

    def on_mount(self)-> None:
        self.switch_mode("lv")


if __name__ == "__main__":
    ModesApp().run()

