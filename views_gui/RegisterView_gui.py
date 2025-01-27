import time
import globals
import customtkinter as ctk
from PIL import Image, ImageTk  # Import to handle image loading

from container import Container


class RegisterView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_controller = Container.getUserController()

        self.controller.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)  # Górny obszar
        self.grid_rowconfigure(1, weight=3)  # Środkowa sekcja
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)  # Dolna sekcja

    # === Title Section ===
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(20, 0))

        # Add Title
        ctk.CTkLabel(title_frame, text="Create Account", font=ctk.CTkFont(size=40, weight="bold"),
                     text_color="#57A6FF").pack(pady=(10, 1), padx=100)
        ctk.CTkLabel(title_frame, text="Register to get started", font=ctk.CTkFont(size=16),
                     text_color="#B3AEAE").pack(pady=(0, 0))

    # === Left Section: Registration Form ===
        form_frame = ctk.CTkFrame(self, fg_color="#323232", width=500, corner_radius=10)
        form_frame.grid(row=1, column=0, sticky="e", pady=(0, 0))

        # Username Field
        ctk.CTkLabel(form_frame, text="Username", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#57A6FF").pack(anchor="w", padx=10, pady=(5, 1))
        username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your username", width=300, height=40)
        username_entry.pack(pady=1, padx=5, anchor="w")

        # Password Field
        ctk.CTkLabel(form_frame, text="Password", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#57A6FF").pack(anchor="w", padx=10, pady=(10, 1))
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your password", width=300, height=40,
                                      show="*")
        password_entry.pack(pady=1, padx=5, anchor="w")

        # Email Field
        ctk.CTkLabel(form_frame, text="Email", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#57A6FF").pack(anchor="w", padx=10, pady=(10, 1))
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your email", width=300, height=40)
        email_entry.pack(pady=1, padx=5, anchor="w")

        # Error/Success Message
        message_label = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=12), text_color="#FF4B4B")
        message_label.pack(pady=2)

        # Register Button
        register_button = ctk.CTkButton(form_frame, text="Register", width=300, height=50, fg_color="#FF4B4B",
                                        text_color="#FFFFFF", font=ctk.CTkFont(size=16, weight="bold"),
                                        hover_color="#FF6961", command=lambda: register_user())
        register_button.pack(pady=5)

        # Back to Login Button
        account_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        account_frame.pack(pady=10)

        ctk.CTkLabel(account_frame, text="Back to ", font=ctk.CTkFont(size=12),
                     text_color="#B3AEAE").pack(side="left")

        ctk.CTkButton(account_frame, text="logging in?", fg_color="#FFFFFF", text_color="#FF4B4B",
                      hover_color="#FFDBDB", font=ctk.CTkFont(size=12), width=70, height=20, border_width=1,
                      command=lambda: controller.show_frame("LogView")
                      ).pack(side="left", padx=5)

    # === Right Section: Image ===
        image = ctk.CTkImage(Image.open('Images/register.png'), size=(350, 350))
        label = ctk.CTkLabel(self, text="", image=image, corner_radius=70)
        label.grid(row=1, column=1, sticky="w", padx=20, pady=20)

        def register_user():
            username = username_entry.get()
            password = password_entry.get()
            email = email_entry.get()

            if not username or not password or not email:
                message_label.configure(text="All fields are required!", text_color="#FF4B4B")
                return

            if "@" not in email or "." not in email:
                message_label.configure(text="Invalid email address!", text_color="#FF4B4B")
                return

            if len(password) < 6:
                message_label.configure(text="Password must be at least 6 characters!", text_color="#FF4B4B")
                return

            # Simulate user creation and transition
            username_entry.configure(border_color="green")
            self.update()
            time.sleep(1)

            password_entry.configure(border_color="green")
            self.update()
            time.sleep(1)

            email_entry.configure(border_color="green")
            self.update()
            time.sleep(1)

            register_button.configure(fg_color="green", hover_color="#6DC066")
            self.update()
            time.sleep(1)

            self.user_controller.create_user(username, password, email)
            message_label.configure(text="Account created successfully!", text_color="#4CAF50")

            userId = self.user_controller.get_id_by_username(username)
            print(userId[0])
            globals.logged_in_user_id = (userId[0])

            def reset_and_transition():
                username_entry.configure(border_color="#CCCCCC")
                password_entry.configure(border_color="#CCCCCC")
                email_entry.configure(border_color="#CCCCCC")
                register_button.configure(fg_color="#FF4B4B", hover_color="#FF6961")
                username_entry.delete(0, "end")
                password_entry.delete(0, "end")
                email_entry.delete(0, "end")
                self.controller.show_frame("DashboardView")

            self.after(1000, reset_and_transition)
