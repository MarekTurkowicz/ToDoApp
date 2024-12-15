import customtkinter as ctk

class AddTask(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Create New Task", font=("Helvetica", 24)).pack(pady=20)

        ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("DashboardView")).pack(pady=10)
