import customtkinter as ctk
from views_gui.AddTaskView_gui import AddTask
from views_gui.DashboardView_gui import DashboardView

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
        for F in (AddTask, DashboardView):
            frame = F(parent=self.container, controller=self)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #default view
        self.show_frame("DashboardView")

    def show_frame(self, page_name):
        frame = self.frame[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
