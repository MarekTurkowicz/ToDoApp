import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        # ctk.CTkLabel(self, text="Dashboard", font=("Helvetica", 24)).pack(pady=20)
        ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size =30, weight="bold")).pack(pady=20)

        scrollable_frame = ctk.CTkScrollableFrame(self, width=500, height=200).pack(pady=20)
        ctk.CTkButton(self, text="Add Task", command=lambda: self.controller.show_frame("AddTask")).pack(pady=10)
