import customtkinter as ctk
from pandas.core.apply import frame_apply

from views.add_task_view import AddTaskView
from views.log_view import LogView
from views.register_view import RegisterView
from views_gui.test_ciew import DashboardView

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title = " To Do App"
        self.geometry("800x600")
        self.resizable(True, True)

    #container for all views
        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.pack(side="top", fill="both", expand=True)

    #directory for views
        self.frame = {}
    #add views
        for F in (AddTaskView, DashboardView, LogView, RegisterView):
            frame = F(parent=self.container, controller=self)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #default view
        self.show_frame(LogView)

    def show_frame(self, page_name):
        frame = self.frame[page_name]
        frame.tkraise()