import os
import subprocess
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
import customtkinter as ctk
from select import select

from container import Container
import globals

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
        control_frame = ctk.CTkFrame(self, fg_color="#373739")
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
            text="Tasks: ",
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
        ).pack(side="right", padx=(10, 10))

        ctk.CTkButton(
            control_frame,
            text="Show Task Pie Chart",
            width=120,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            text_color="#FFFFFF",
            command=self.open_pie_chart_window
        ).pack(side="right", padx=(10, 10))




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

        ctk.CTkButton(
            control_frame,
            text="Run Console Mode",
            width=120,
            fg_color="#1E88E5",
            hover_color="#1565C0",
            text_color="#FFFFFF",
            command=lambda: self.run_console_mode()
        ).pack(side="right", padx=(10, 10))

    def load_tasks(self, status="to_do"):
        """Load tasks dynamically into the scrollable frame."""
        self.update_idletasks()
        self.update()
        print(f' z dashboardu{globals.logged_in_user_id}')
        tasks = self.task_controller.get_tasks_by_user_id(globals.logged_in_user_id)

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
        task_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#333333", corner_radius=10)
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
            text_color = "#B3AEAE",
            anchor="w",
        ).pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            left_frame,
            text=f"{task.description}",
            font=ctk.CTkFont(size=12),
            text_color = "#B3AEAE",
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
            command=lambda t=task: self.open_edit_task_window(t),
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

    def open_edit_task_window(self, task):
        """Otwiera okno Toplevel do edycji taska (usunięcie starego i dodanie nowego)."""
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit Task")
        edit_window.geometry("400x400")
        edit_window.grab_set()

        # Zmienne do aktualizacji taska
        title_var = ctk.StringVar(value=task.title)
        description_var = ctk.StringVar(value=task.description)
        date_var = ctk.StringVar(value=task.due_date.strftime("%Y-%m-%d"))

        # Nagłówek
        ctk.CTkLabel(edit_window, text="Edit Task", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#1E88E5").pack(pady=10)

        # Tytuł
        ctk.CTkLabel(edit_window, text="Title:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(5, 0))
        title_entry = ctk.CTkEntry(edit_window, textvariable=title_var, width=300)
        title_entry.pack(padx=20, pady=5)

        # Opis
        ctk.CTkLabel(edit_window, text="Description:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(5, 0))
        description_entry = ctk.CTkEntry(edit_window, textvariable=description_var, width=300)
        description_entry.pack(padx=20, pady=5)

        # Data
        ctk.CTkLabel(edit_window, text="Due Date (yyyy-mm-dd):", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20,
                                                                                                 pady=(5, 0))
        date_entry = ctk.CTkEntry(edit_window, textvariable=date_var, width=300)
        date_entry.pack(padx=20, pady=5)

        # Przycisk zapisywania zmian
        def save_changes():
            try:
                # Pobierz nowe dane z formularza
                new_title = title_var.get()
                new_description = description_var.get()
                new_due_date = datetime.strptime(date_var.get(), "%Y-%m-%d")

                # Usuń stare zadanie
                self.task_controller.delete_task(task.id)

                # Dodaj nowe zadanie
                self.task_controller.add_task(new_title, new_description, new_due_date, task.user_id)

                # Odśwież widok tasków
                self.load_tasks(status="to_do" if not self.task_switch.get() else "done")
                edit_window.destroy()
            except ValueError:
                error_label.configure(text="Invalid date format! Use yyyy-mm-dd.", text_color="#E53935")

        ctk.CTkButton(edit_window, text="Save Changes", fg_color="#43A047", hover_color="#388E3C",
                      text_color="#FFFFFF", command=save_changes).pack(pady=20)

        # Przycisk zamknięcia
        ctk.CTkButton(edit_window, text="Cancel", fg_color="#FF4B4B", hover_color="#FF6961",
                      text_color="#FFFFFF", command=edit_window.destroy).pack()

        # Etykieta błędu
        error_label = ctk.CTkLabel(edit_window, text="", font=ctk.CTkFont(size=12))
        error_label.pack(pady=5)

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
        """Otwiera okno Toplevel z wykresem słupkowym ilości tasków na dzień."""
        # Pobierz dane tasków
        tasks = self.task_controller.get_tasks_by_user_id(globals.logged_in_user_id)
        task_dates = [task.due_date.date() for task in tasks]
        date_counts = Counter(task_dates)

        # Przygotuj dane do wykresu
        sorted_dates = sorted(date_counts.keys())
        task_counts = [date_counts[date] for date in sorted_dates]

        # Stwórz wykres
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100, facecolor="#333333")
        colors = ["#FF4B4B", "#4CAF50", "#57A6FF", "#FBC02D", "#9C27B0"]

        ax.bar(
            sorted_dates, task_counts, color=[colors[i % len(colors)] for i in range(len(task_counts))], width=1.5
        )

        # Ustawienia wykresu
        ax.set_facecolor("#393939")  # Ciemne tło osi wykresu
        ax.set_title("Tasks Over Time", fontsize=14, fontweight="bold", color="#FFFFFF")  # Biały tekst
        ax.set_xlabel("Date", fontsize=12, color="#FFFFFF")
        ax.set_ylabel("Number of Tasks", fontsize=12, color="#FFFFFF")

        # Ustawienia osi Y
        ax.set_yticks(range(max(task_counts) + 2))
        ax.tick_params(axis='x', colors="#FFFFFF")  # Białe numery na osi X
        ax.tick_params(axis='y', colors="#FFFFFF")  # Białe numery na osi Y

        ax.grid(False)  # Usuń siatkę

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
            text_color="#FFFFFF", command=chart_window.destroy
        ).pack(pady=10)

    def on_show(self):
        """Funkcja odświeżająca widok Dashboard przy jego aktywacji."""
        print("Refreshing dashboard...")
        self.load_tasks(status="to_do" if not self.task_switch.get() else "done")

    def run_console_mode(self):
        """Uruchamia tryb konsolowy i zamyka GUI."""
        # Ścieżka do katalogu głównego
        base_path = r"C:\Users\xBrav\PycharmProjects\KCK"  # Zdefiniowana ścieżka projektu
        main_script = os.path.join(base_path, "main.py")  # Pełna ścieżka do main.py

        # Komenda do uruchomienia nowego procesu w nowym oknie konsoli
        command = [sys.executable, main_script, "-c"]  # Użycie tego samego interpretera Pythona

        # Uruchom proces w nowym oknie konsoli
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=base_path)

        # Zamykanie GUI
        self.quit()  # Zamyka aplikację Tkinter

    def open_pie_chart_window(self):
        """Otwiera okno Toplevel z wykresem kołowym podziału tasków (zrobione vs niezrobione)."""
        # Pobierz dane tasków
        tasks = self.task_controller.get_tasks_by_user_id(globals.logged_in_user_id)

        # Policz zrobione i niezrobione taski
        completed_tasks = sum(task.is_completed for task in tasks)
        incomplete_tasks = len(tasks) - completed_tasks

        if len(tasks) == 0:
            # Jeśli brak tasków, wyświetl komunikat
            no_task_window = ctk.CTkToplevel(self)
            no_task_window.title("Task Pie Chart")
            no_task_window.geometry("400x200")
            no_task_window.grab_set()

            ctk.CTkLabel(
                no_task_window, text="No tasks available to show!", font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=50)

            ctk.CTkButton(
                no_task_window, text="Close", fg_color="#FF4B4B", hover_color="#FF6961",
                text_color="#FFFFFF", command=no_task_window.destroy
            ).pack(pady=10)
            return

        # Przygotuj dane do wykresu
        labels = ["Completed", "To Do"]
        sizes = [completed_tasks, incomplete_tasks]
        colors = ["#4CAF50", "#FF4B4B"]  # Zielony dla zrobionych, czerwony dla niezrobionych

        # Tworzenie wykresu
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor="#333333")
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.1f%%", startangle=140,
            colors=colors, textprops=dict(color="white"), wedgeprops=dict(edgecolor="#222222")
        )

        ax.set_title("Tasks Status", fontsize=14, color="#FFFFFF", fontweight="bold")

        # Okno Toplevel
        pie_window = ctk.CTkToplevel(self)
        pie_window.title("Task Status Pie Chart")
        pie_window.geometry("600x500")
        pie_window.grab_set()

        # Umieszczenie wykresu w oknie
        canvas = FigureCanvasTkAgg(fig, master=pie_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Przycisk zamykający okno
        ctk.CTkButton(
            pie_window, text="Close", fg_color="#FF4B4B", hover_color="#FF6961",
            text_color="#FFFFFF", command=pie_window.destroy
        ).pack(pady=10)
