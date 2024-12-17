import customtkinter as ctk
from tkinter import StringVar
from datetime import datetime, timedelta
import calendar


class AddTaskView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Zmienne do przechowywania danych
        self.title_var = StringVar()
        self.description_var = StringVar()
        self.date_var = StringVar(value="No date selected")  # Domyślna wartość daty

        # Nagłówek
        ctk.CTkLabel(self, text="Add New Task", font=ctk.CTkFont(size=30, weight="bold"),
                     text_color="#1E88E5").pack(pady=20)

        # Sekcja formularza
        form_frame = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10, border_color="#BDBDBD", border_width=1)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Pole na tytuł
        ctk.CTkLabel(form_frame, text="Title:", font=ctk.CTkFont(size=14), text_color="#FFFFFF").pack(anchor="w", padx=20, pady=(10, 0))
        self.title_entry = ctk.CTkEntry(form_frame, textvariable=self.title_var, width=400, fg_color="#343434",
                                        border_color="#BDBDBD", border_width=1)
        self.title_entry.pack(padx=20, pady=5)

        # Pole na opis
        ctk.CTkLabel(form_frame, text="Description:", font=ctk.CTkFont(size=14), text_color="#FFFFFF").pack(anchor="w", padx=20, pady=(10, 0))
        self.description_entry = ctk.CTkEntry(form_frame, textvariable=self.description_var, width=400, fg_color="#343434",
                                              border_color="#BDBDBD", border_width=1)
        self.description_entry.pack(padx=20, pady=5)

        # Przycisk do wyboru daty
        ctk.CTkButton(form_frame, text="Select Date", fg_color="#1E88E5", hover_color="#1565C0",
                      text_color="#FFFFFF", command=self.open_date_window).pack(pady=10)

        # Etykieta pokazująca wybraną datę
        self.date_label = ctk.CTkLabel(form_frame, textvariable=self.date_var,
                                       font=ctk.CTkFont(size=14), text_color="#757575")
        self.date_label.pack(pady=5)

        # Przycisk do dodania zadania
        ctk.CTkButton(self, text="Add Task", fg_color="#43A047", hover_color="#388E3C",
                      text_color="#FFFFFF", command=self.add_task, width=200).pack(pady=20)

        # Przycisk do dodania zadania
        ctk.CTkButton(self, text="Powrót", fg_color="#43A047", hover_color="#388E3C",
                      text_color="#FFFFFF", command=lambda: controller.show_frame("DashboardView"), width=200).pack(pady=20)

    def open_date_window(self):
        """Otwiera ogólne okno CTkToplevel z opcjami szybkiego wyboru daty."""
        date_window = ctk.CTkToplevel(self)
        date_window.title("Select Date")
        date_window.geometry("500x600")
        date_window.grab_set()  # Okno modalne

        # Nagłówek
        ctk.CTkLabel(date_window, text="Select a Date", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#4A90E2").pack(pady=10)

        # --- Szybki wybór kolejnych dni tygodnia ---
        ctk.CTkLabel(date_window, text="Quick Select - Next:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        quick_dates_frame = ctk.CTkFrame(date_window, fg_color="transparent")
        quick_dates_frame.pack()

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        def set_quick_date(day_name):
            today = datetime.now()
            days_ahead = (list(calendar.day_name).index(day_name) - today.weekday()) % 7
            days_ahead = days_ahead or 7  # Jeśli wybrany dzień to dzisiaj, przesuwamy na następny tydzień
            selected_date = today + timedelta(days=days_ahead)
            self.date_var.set(selected_date.strftime("%Y-%m-%d"))
            date_window.destroy()

        # Przycisk dla każdego dnia tygodnia
        for day in days_of_week:
            ctk.CTkButton(quick_dates_frame, text=f"{day}", width=50, fg_color="#4A90E2",
                          hover_color="#6FB6FF", command=lambda d=day: set_quick_date(d)).pack(side="left", padx=1)

        # --- Sekcja wyboru dnia tygodnia i liczby tygodni ---
        ctk.CTkLabel(date_window, text="Custom Select:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Dropdown dla dnia tygodnia
        ctk.CTkLabel(date_window, text="Choose a day of the week:").pack(pady=5)
        selected_day = StringVar(value=days_of_week[0])  # Domyślnie Monday
        day_dropdown = ctk.CTkOptionMenu(date_window, variable=selected_day, values=days_of_week)
        day_dropdown.pack(pady=5)

        # Wybór liczby tygodni
        ctk.CTkLabel(date_window, text="In how many weeks?").pack(pady=5)
        weeks_entry = ctk.CTkEntry(date_window, placeholder_text="Enter weeks (e.g., 1, 2, 3)", width=200)
        weeks_entry.pack(pady=5)

        # Funkcja obliczająca datę
        def calculate_custom_date():
            try:
                weeks = int(weeks_entry.get()) if weeks_entry.get().isdigit() else 0
                today = datetime.now()
                day_name = selected_day.get()
                days_ahead = (list(calendar.day_name).index(day_name) - today.weekday()) % 7
                days_ahead = days_ahead or 7  # Najbliższy dzień

                # Obliczenie daty
                target_date = today + timedelta(days=days_ahead + weeks * 7)
                self.date_var.set(target_date.strftime("%Y-%m-%d"))
                date_window.destroy()
            except Exception as e:
                error_label.configure(text="Invalid input! Weeks must be a number.", text_color="red")

        ctk.CTkButton(date_window, text="Set Date", fg_color="#4A90E2", hover_color="#6FB6FF",
                      command=calculate_custom_date).pack(pady=10)

        # --- Ręczne wpisanie daty ---
        ctk.CTkLabel(date_window, text="Or enter a date manually:", font=ctk.CTkFont(size=14)).pack(pady=10)
        manual_date_entry = ctk.CTkEntry(date_window, placeholder_text="yyyy-mm-dd", width=200)
        manual_date_entry.pack(pady=5)

        # Walidacja ręcznie wpisanej daty
        def submit_manual_date():
            try:
                manual_date = datetime.strptime(manual_date_entry.get(), "%Y-%m-%d")
                self.date_var.set(manual_date.strftime("%Y-%m-%d"))
                date_window.destroy()
            except ValueError:
                error_label.configure(text="Invalid date format! Use yyyy-mm-dd.", text_color="red")

        ctk.CTkButton(date_window, text="Submit Date", fg_color="#4A90E2", hover_color="#6FB6FF",
                      command=submit_manual_date).pack(pady=10)

        # Etykieta na błędy
        error_label = ctk.CTkLabel(date_window, text="", font=ctk.CTkFont(size=12))
        error_label.pack()

    def add_task(self):
        """Przesyła zadanie do kontrolera."""
        title = self.title_var.get()
        description = self.description_var.get()
        due_date_str = self.date_var.get()

        # Walidacja daty
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Please select a date.")
            return

        user_id = self.controller.logged_in_user_id  # Pobierz ID zalogowanego użytkownika
        print(f'{user_id}')
        # Sprawdzenie, czy pola są wypełnione
        if title and description and due_date:
            self.controller.task_controller.add_task(title, description, due_date, user_id)
            print(f"Task Added: {title}, {description}, {due_date}, User ID: {user_id}")
            self.clear_form()
        else:
            print("All fields are required!")

    def clear_form(self):
        """Czyści formularz po dodaniu zadania."""
        self.title_var.set("")
        self.description_var.set("")
        self.date_var.set("No date selected")
