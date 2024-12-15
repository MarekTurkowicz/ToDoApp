import customtkinter as ctk
from container import Container

class RegisterView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_controller = Container.getUserController()


        #ctk.CTkLabel(self, text="Register ", font=("Helvetica", 24)).pack(pady=20)

        # Layout
        self.grid_columnconfigure(0, weight=1)  # Center the form horizontally
        self.grid_rowconfigure(0, weight=1)

        # === Registration Form ===
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            form_frame, text="Create an Account", font=ctk.CTkFont(size=36, weight="bold"), text_color="#0176FC"
        ).pack(pady=10)

        # Username Field
        ctk.CTkLabel(
            form_frame, text="Username", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0176FC"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your username", width=300, height=40)
        self.username_entry.pack(pady=5)

        # Password Field
        ctk.CTkLabel(
            form_frame, text="Password", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0176FC"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your password", width=300, height=40,
                                           show="*")
        self.password_entry.pack(pady=5)

        # Email Field
        ctk.CTkLabel(
            form_frame, text="Email", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0176FC"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your email", width=300, height=40)
        self.email_entry.pack(pady=5)

        # Error/Success Message
        self.message_label = ctk.CTkLabel(
            form_frame, text="", font=ctk.CTkFont(size=12), text_color="#FF4B4B"
        )
        self.message_label.pack(pady=10)

        # Register Button
        ctk.CTkButton(
            form_frame, text="Register", width=300, height=50, fg_color="#FF4B4B", text_color="#FFFFFF",
            font=ctk.CTkFont(size=16, weight="bold"), hover_color="#FF6961",
            command=self.register_user
        ).pack(pady=20)

        # Back to Login Button
        ctk.CTkButton(
            form_frame, text="Back to Login", width=300, height=40, fg_color="#FFFFFF", text_color="#0176FC",
            font=ctk.CTkFont(size=14), hover_color="#E1E8FF",
            command=lambda: controller.show_frame("LogView")
        ).pack(pady=5)


        # ctk.CTkButton(self, text="Go to dashboard", command=lambda: controller.show_frame("DashboardView")).pack(pady=10)


    def register_user(self):
        """Register a new user."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        self.password_entry.delete(0, "end")

        # Simulated validation and registration logic
        if not username or not password or not email:
            self.message_label.configure(text="All fields are required!", text_color="#FF4B4B")
        elif "@" not in email or "." not in email:
            self.message_label.configure(text="Invalid email address!", text_color="#FF4B4B")
        elif len(password) < 6:
            self.message_label.configure(text="Password must be at least 6 characters!", text_color="#FF4B4B")
        elif  self.user_controller.get_user_by_username_and_password(username, password):
            self.message_label.configure(text="This user exist - sign in!", text_color="#FF4B4B")
        else:
            # Simulate saving user to a database
            self.message_label.configure(text="Account created successfully!", text_color="#4CAF50")
            print(f"User Registered: {username}, {email}")
            # Optionally clear fields after successful registration
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.email_entry.delete(0, "end")

            self.user_controller.create_user(username, password, email)
            userChecked = self.user_controller.get_user_by_username_and_password(username, password)
            self.controller.logged_in_user = userChecked.username
            self.controller.logged_in_id = userChecked.id
            print(f"Zarejestrowano i zalogownao użytkownika: {userChecked.username} (ID: {userChecked.id})")
            self.controller.show_frame("DashboardView")


