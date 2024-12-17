import time
import globals
import customtkinter as ctk
from PIL import Image, ImageTk  # Import to handle image loading

from container import Container


class LogView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_controller = Container.getUserController()

        self.controller.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)  # Górny obszar
        self.grid_rowconfigure(1, weight=3)  # Środkowa sekcja
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)  # dolna sekcja

    # === middle Section: welcome Form ===
        welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        welcome_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(20, 0))

        # Add Title
        ctk.CTkLabel(welcome_frame, text="Welcome Back!", font=ctk.CTkFont(size=40, weight="bold"),
                     text_color="#57A6FF").pack(pady=(10, 1), padx=100)
        ctk.CTkLabel(welcome_frame, text="Sign in to continue", font=ctk.CTkFont(size=16), text_color="#B3AEAE").pack(
            pady=(0, 0))

    # === Left Section: Login Form ===
        form_frame = ctk.CTkFrame(self, fg_color="#323232", width=500, corner_radius=10)
        form_frame.grid(row=1, column=0, sticky="e", pady=(0, 0))  # Place in left column

        # Add Login Entry Field
        ctk.CTkLabel(form_frame, text="Username/Login", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#57A6FF").pack(anchor="w", padx=10, pady=(5, 1))
        login_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your username", width=300, height=40)
        login_entry.pack(pady=1, padx=5, anchor="w")

        # Add Password Entry Field
        ctk.CTkLabel(form_frame, text="Password", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#57A6FF").pack(anchor="w", padx=10, pady=(10, 1))
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your password", width=300, height=40,
                                      show="*")
        password_entry.pack(pady=1, padx=5, anchor="w")

        # Forgot Password
        ctk.CTkLabel(form_frame, text="Forgot your password?", font=ctk.CTkFont(size=10),
                     text_color="#B3AEAE").pack(anchor="w", padx=15, pady=0)

        # Komunikat o błędzie (domyślnie ukryty)
        message_label = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=12), text_color="#FF4B4B")
        message_label.pack(pady=2)

        # Add Sign-in Button
        sign_in_button = ctk.CTkButton(form_frame, text="Sign in", width=300, height=50, fg_color="#FF4B4B",
                                       text_color="#FFFFFF",
                                       font=ctk.CTkFont(size=16, weight="bold"), hover_color="#FF6961",
                                       command=lambda: verifyLogin())
        sign_in_button.pack(pady=5)

        # Create Account Section
        account_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        account_frame.pack(pady=10)

        ctk.CTkLabel(account_frame, text="Don’t have an Account?", font=ctk.CTkFont(size=12),
                     text_color="#B3AEAE").pack(side="left")

        ctk.CTkButton(account_frame, text="Create account", fg_color="#FFFFFF", text_color="#FF4B4B",
                      hover_color="#FFDBDB", font=ctk.CTkFont(size=12), width=70, height=20, border_width=1,
                      command=lambda: controller.show_frame("RegisterView")
                      ).pack(side="left", padx=5)

    # === Right Section: Image ===
        image = ctk.CTkImage(Image.open('Images/login.png'), size=(300, 300))
        label = ctk.CTkLabel(self, text="", image=image, corner_radius=70)
        label.grid(row=1, column=1, sticky="w", padx=20, pady=20)  # Place in the right column

        def verifyLogin():
            login = login_entry.get()
            password = password_entry.get()
            userChecked = self.user_controller.get_user_by_username_and_password(login, password)
            userId = self.user_controller.get_id_by_username(login)
            if userChecked:
                # Zmiana kolorów obwódek i przycisku na zielone z przerwami
                login_entry.configure(border_color="green")
                self.update()
                time.sleep(1)

                password_entry.configure(border_color="green")
                self.update()
                time.sleep(1)

                sign_in_button.configure(fg_color="green", hover_color="#6DC066")
                self.update()
                time.sleep(1)

                message_label.configure(text="Signed in successfully!", text_color="#4CAF50")

                globals.logged_in_user_id = int(userId[0])
                self.controller.logged_in_username = userChecked.username


                print(f' log log view id - pobierana : {userId[0]}')
                print(f' log log view id: {globals.logged_in_user_id}')


                message_label.configure(text="")
                login_entry.delete(0, "end")
                password_entry.delete(0, "end")

                # Przejście do DashboardView po przerwie
                def reset_and_transition():
                    # Przywróć kolory po przejściu
                    login_entry.configure(border_color="#CCCCCC")
                    password_entry.configure(border_color="#CCCCCC")
                    sign_in_button.configure(fg_color="#FF4B4B", hover_color="#FF6961")
                    self.controller.show_frame("DashboardView")

                self.after(1000, reset_and_transition)
            else:
                message_label.configure(text="Invalid username or password!")
