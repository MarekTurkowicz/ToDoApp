import customtkinter as ctk

from container import Container

from views_gui.AddTaskView_gui import AddTaskView
from views_gui.DashboardView_gui import DashboardView
from views_gui.LogView_gui import LogView
from views_gui.RegisterView_gui import RegisterView

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

    #db,controllers,log vars
        Container.getDbConnection()
        self.user_controller = Container.getUserController()
        self.task_controller = Container.getTaskController()
        self.logged_in_user = None
        self.logged_in_user_id = None

    #window
        self.title("To Do App")
        self.geometry("800x600")
        self.resizable(True, True)
        ctk.set_default_color_theme("dark-blue")


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

    # Configure the grid to make all views centered
            self.container.grid_rowconfigure(0, weight=1)
            self.container.grid_columnconfigure(0, weight=1)

    #default view
        self.show_frame("LogView")

    def show_frame(self, page_name):
        frame = self.frame[page_name]
        frame.tkraise()
        if page_name == "DashboardView":
            self.geometry("1080x800")
        elif page_name == "LogView":
            self.geometry("800x600")
        elif page_name == "RegisterView":
            self.geometry("800x600")
        elif page_name == "AddTaskView":
            self.geometry("800x600")

    def set_logged_in_user_username(self, user):
        """Set logged user name."""
        self.logged_in_user = user

    def set_logged_in_user_id(self, id):
        """Set logged user id."""
        self.logged_in_user_id = id

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
