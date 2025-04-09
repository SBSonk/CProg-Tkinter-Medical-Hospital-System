import tkinter as tk
import models
from sqlalchemy.orm import Session
from sqlalchemy import Select
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window
from PIL import Image, ImageTk  # Importing PIL modules

class Login(tk.Frame):
    ent_username: PlaceholderEntry = None
    ent_password: PlaceholderEntry = None
    btn_login: tk.Button = None

    login_success = None
    login_fail = None

    session: Session = None

    def login(self):
        # validate entries
        if not self.ent_username or not self.ent_password:
            showinfo('Alert', 'Entry widgets not initialized.')
            return
        
        username = self.ent_username.get_text()
        password = self.ent_password.get_text()

        # Validate input
        if not username or not password:
            showinfo('Alert', 'Empty fields.')
            return

        try:
            statement = Select(models.User).where(models.User.username == username)
            user: models.User = self.session.execute(statement).scalar_one_or_none()
            
            if not user:
                showinfo('Alert', 'User does not exist.')
                if callable(self.login_fail):
                    self.login_fail()
                    return
            
            if user.check_password(password):
                showinfo('Alert', 'Logged in successfully.')
                switch_to_window("main_menu", onCreateArgs=(user,))
                if callable(self.login_success):
                    self.login_success()
            else:
                showinfo('Alert', 'Incorrect password.')
                if callable(self.login_fail):
                    self.login_fail()
        except Exception as e:
            print(f'Login error: {e}')
            if callable(self.login_fail):
                self.login_fail()

    def __init__(self, master, session: Session, login_success=None, login_fail=None):
        super().__init__(master)
        self.session = session
        self.login_success = login_success
        self.login_fail = login_fail

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)
        
        # Left Column (Logo)
        left_frame = tk.Frame(frame, width=150, height=540)
        left_frame.grid(row=0, column=0, rowspan=6, padx=10)
        
        # Resize logo using PIL
        logo_image = Image.open("icons/vcl.png")  # Open the image file
        logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_image)  # Convert the resized image to a format Tkinter can use
        
        logo_label = tk.Label(left_frame, image=logo_image)
        logo_label.image = logo_image  # Keep a reference to the image to avoid garbage collection
        logo_label.pack(pady=50)  # Adjust padding as needed

        # Right Column (Form Elements)
        right_frame = tk.Frame(frame, width=234, height=540)
        right_frame.grid(row=0, column=1, rowspan=6, padx=10)
        
        ttk.Label(right_frame, text='Login', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)

        self.ent_username = PlaceholderEntry(right_frame, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Username', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_username.grid(row=1, column=0, ipady=7.5)

        self.ent_password = PlaceholderEntry(right_frame, 
                                             is_password=True, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password.grid(row=2, column=0, ipady=7.5)

        HyperlinkLabel(right_frame, 
                       text='Forgot Password?', 
                       on_click=lambda x: switch_to_window('forget_password'),
                       default_color='gray',
                       hover_color='black').grid(row=3, column=0, pady=0, sticky='w')

        self.btn_login = ttk.Button(right_frame, text='Login', padding=(87.5, 12.5), command=self.login)
        self.btn_login.grid(row=4, column=0, pady=10)

        back_button = ttk.Button(right_frame, text="Back", command=self.go_back)
        back_button.grid(row=5, column=0, pady=10, sticky='sw')

        frame.pack(padx=15, pady=15)
        
    def go_back(self):
        switch_to_window('landing')
