from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
import customtkinter as ctk
from container import Container


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_controller = Container.getUserController()
        self.task_controller = Container.getTaskController()


        # === Header Section ===
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 5))

        ctk.CTkLabel(
            header_frame, text="Dashboard", font=ctk.CTkFont(size=40, weight="bold"),text_color="#57A6FF"
        ).pack(pady=20)

        # === Buttons and Switch Section ===
        control_frame = ctk.CTkFrame(self, fg_color="#333333")
        control_frame.pack(fill="x", pady=10, padx=10)

        # Add Task Button
        ctk.CTkButton(
            control_frame,
            text="Add Task",
            width=120,
            command=lambda: self.controller.show_frame("AddTaskView"),
        ).pack(side="left", padx=(10, 20))

        # Task Switch (To Do / Done)
        switch_label = ctk.CTkLabel(
            control_frame,
            text="Todo:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        switch_label.pack(side="left")

        self.task_switch = ctk.CTkSwitch(
            control_frame,
            text="",
            command=self.switch_task_view,
        )
        self.task_switch.pack(side="left", padx=2)

        self.switch_status_label = ctk.CTkLabel(
            control_frame,
            text="Done",
            font=ctk.CTkFont(size=14)
        )
        self.switch_status_label.pack(side="left")

        ctk.CTkButton(
            control_frame,
            text="Show Task Chart",
            width=120,
            fg_color="#1E88E5",
            hover_color="#1565C0",
            text_color="#FFFFFF",
            command=self.open_task_chart_window
        ).pack(side="right", padx=(10, 0))

        # === Scrollable Task Section ===
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=1050, height=500)
        self.scrollable_frame.pack(pady=10, padx=10)

        # Load Tasks
        self.load_tasks(status="to_do")

        # === Footer Section ===
        footer_frame = ctk.CTkFrame(self, fg_color="#333333")
        footer_frame.pack(fill="x", pady=(20, 10), padx=10)

        ctk.CTkButton(
            footer_frame, text="Back to Login",
            command=lambda: self.controller.show_frame("LogView")
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            footer_frame, text="Exit App", fg_color="#FF4B4B", hover_color="#FF6961",
            command=controller.quit
        ).pack(side="right", padx=10)

    def load_tasks(self, status="to_do"):
        """Load tasks dynamically into the scrollable frame."""
        tasks = self.task_controller.get_tasks_by_user_id(1)

        # Filtrowanie tasków w zależności od is_completed
        if status == "to_do":
            tasks = [task for task in tasks if not task.is_completed]
        else:
            tasks = [task for task in tasks if task.is_completed]

        # Clear previous tasks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not tasks:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No tasks available",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#888888",
            ).pack(pady=10)
            return

        for task in tasks:
            self.create_task_frame(task)

    def create_task_frame(self, task):
        """Create a task frame with details and actions."""
        task_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E1E8FF", corner_radius=10)
        task_frame.pack(fill="x", pady=5, padx=5)

        # Split the content into two columns
        content_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=(5, 5))

        # Left Section: Title and Description
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            left_frame,
            text=f"{task.title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333",
            anchor="w",
        ).pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            left_frame,
            text=f"{task.description}",
            font=ctk.CTkFont(size=12),
            text_color="#555555",
            anchor="w",
        ).pack(fill="x")

        # Right Section: Due Date and Buttons
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=(10, 0))

        formatted_date = task.due_date.strftime("%Y-%m-%d")
        ctk.CTkLabel(
            right_frame,
            text=f"Due: {formatted_date}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FF5733",
        ).pack()

        # Buttons below the due date
        button_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(
            button_frame,
            text="Edit",
            width=60,
            command=lambda t=task: self.edit_task(t),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Delete",
            width=60,
            fg_color="#FF4B4B",
            hover_color="#FF6961",
            command=lambda t=task: self.delete_task(t),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="●",
            width=40,
            height=40,
            fg_color="#4CAF50",
            text_color="#FFFFFF",
            command=lambda t=task: self.toggle_task_status(t),
        ).pack(side="left", padx=5)
    def switch_task_view(self):
        """Switch between To Do and Done tasks."""
        status = "done" if self.task_switch.get() else "to_do"
        self.switch_status_label.configure(text="Done" if status == "done" else "To Do")
        self.load_tasks(status)

    def toggle_task_status(self, task):
        """Mark task as completed or not completed."""
        self.task_controller.mark_task_completed(task.id)
        self.load_tasks(status="to_do" if not self.task_switch.get() else "done")

    def edit_task(self, task):
        """Edit task - navigate to edit view or open task in form."""
        print(f"Edit Task: {task.title}")

    def delete_task(self, task):
        """Delete task and refresh the list."""
        print(f"Delete Task: {task.title}")
        self.task_controller.delete_task(task.id)
        self.load_tasks(status="to_do" if not self.task_switch.get() else "done")

    def open_task_chart_window(self):
        """Otwiera okno Toplevel z wykresem ilości tasków na dzień."""
        # Pobierz dane tasków
        tasks = self.task_controller.get_tasks_by_user_id(1)
        task_dates = [task.due_date.date() for task in tasks]  # Zbierz daty tasków
        date_counts = Counter(task_dates)  # Policz ilość tasków dla każdej daty

        # Przygotuj dane do wykresu
        sorted_dates = sorted(date_counts.keys())
        task_counts = [date_counts[date] for date in sorted_dates]

        # Stwórz wykres
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(sorted_dates, task_counts, marker="o", linestyle="-", color="#1E88E5")
        ax.set_title("Tasks Over Time", fontsize=14, fontweight="bold", color="#1E88E5")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Number of Tasks", fontsize=12)
        ax.grid(True)

        # Okno Toplevel
        chart_window = ctk.CTkToplevel(self)
        chart_window.title("Task Chart")
        chart_window.geometry("600x500")
        chart_window.grab_set()

        # Umieszczenie wykresu w oknie
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Przycisk zamykający okno
        ctk.CTkButton(
            chart_window, text="Close", fg_color="#FF4B4B", hover_color="#FF6961",
            command=chart_window.destroy
        ).pack(pady=10)
