import customtkinter as ctk
from PIL import Image, ImageTk  # Import to handle image loading

from container import Container


class LogView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_controller = Container.getUserController()


        # Configure grid to divide into two sections: Left (form) and Right (image)
        self.grid_columnconfigure(0, weight=1)  # Left column for the form
        self.grid_columnconfigure(1, weight=1)  # Right column for the image
        self.grid_rowconfigure(0, weight=1)     # Row to center vertically

        # === Left Section: Login Form ===
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Place in left column

        # Add Title
        ctk.CTkLabel(
            form_frame, text="Welcome Back!", font=ctk.CTkFont(size=36, weight="bold"), text_color="#0176FC"
        ).pack(pady=10)

        ctk.CTkLabel(
            form_frame, text="Sign in to continue", font=ctk.CTkFont(size=16), text_color="#B3AEAE"
        ).pack(pady=10)

    # Add Login Entry Field
        ctk.CTkLabel(
            form_frame, text="Login", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0176FC"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        login_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your username", width=300, height=40)
        login_entry.pack(pady=5)

        # Add Password Entry Field
        ctk.CTkLabel(
            form_frame, text="Password", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0176FC"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your password", width=300, height=40, show="*")
        password_entry.pack(pady=5)

        # Komunikat o błędzie (domyślnie ukryty)
        self.error_label = ctk.CTkLabel(
            form_frame, text="", font=ctk.CTkFont(size=12), text_color="#FF4B4B"
        )
        self.error_label.pack(pady=10)

        # Forgot Password
        ctk.CTkLabel(
            form_frame, text="Forgot your password?", font=ctk.CTkFont(size=12), text_color="#B3AEAE"
        ).pack(anchor="w", padx=10, pady=10)

        # Add Sign-in Button
        ctk.CTkButton(
            form_frame, text="Sign in", width=300, height=50, fg_color="#FF4B4B", text_color="#FFFFFF",
            font=ctk.CTkFont(size=16, weight="bold"), hover_color="#FF6961",
            command=lambda: verifyLogin()
        ).pack(pady=20)

        # Create Account Section
        account_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        account_frame.pack(pady=10)

        ctk.CTkLabel(
            account_frame, text="Don’t have an Account?", font=ctk.CTkFont(size=12), text_color="#B3AEAE"
        ).pack(side="left")

        ctk.CTkButton(
            account_frame, text="Create account", fg_color="#FFFFFF", text_color="#FF4B4B",
            hover_color="#FFDBDB", font=ctk.CTkFont(size=12), width=100, height=20, border_width=1,
            command=lambda: controller.show_frame("RegisterView")
        ).pack(side="left", padx=5)

        # === Right Section: Image ===

        image = ctk.CTkImage(Image.open('Images/login.png'), size=(400, 400))
        label = ctk.CTkLabel(self, text="",image=image,  corner_radius=30)
        label.grid(row=0, column=1, sticky="e", padx=20, pady=20)  # Place in the right column


        def verifyLogin():
            login = login_entry.get()
            password = password_entry.get()
            userChecked = self.user_controller.get_user_by_username_and_password(login, password)
            if userChecked:
                self.error_label.configure(text="")  # Wyczyść błąd
                login_entry.delete(0, "end")
                password_entry.delete(0, )
                self.controller.logged_in_user = userChecked.username
                self.controller.logged_in_id = userChecked.id
                print(f"Zalogowano użytkownika: {userChecked.username} (ID: {userChecked.id})")

                self.controller.show_frame("DashboardView")
            else:
                self.error_label.configure(text="Invalid username or password!")
