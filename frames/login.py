import tkinter as tk
import models
from sqlalchemy.orm import Session
from sqlalchemy import Select
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

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
            print('Entry widgets not initialized.')
            return
        
        username = self.ent_username.get_text()
        password = self.ent_password.get_text()

        # Validate input
        if not username or not password:
            print('Empty fields.')
            return

        try:
            statement = Select(models.User).where(models.User.username == username)
            user: models.User = self.session.execute(statement).scalar_one_or_none()
            
            if not user:
                print('User does not exist.')
                if callable(self.login_fail):
                    self.login_fail()
                    return
            
            if user.check_password(password):
                print('Logged in successfully.')
                switch_to_window("main_menu")
                if callable(self.login_success):
                    self.login_success()
            else:
                print('Incorrect password.')
                if callable(self.login_fail):
                    self.login_fail()
        except Exception as e:
            print(f'Database error: {e}')
            if callable(self.login_fail):
                self.login_fail()

    def __init__(self, master, session: Session, login_success = None, login_fail = None):
        super().__init__(master)
        self.session = session
        self.login_success = login_success
        self.login_fail = login_fail

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0)
        frame.grid_rowconfigure(1, pad=20)
        frame.grid_rowconfigure(2, pad=20)
        ttk.Label(frame, text='Login', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)

        # ttk.Label(fr_text, text='Username').pack(anchor='w')
        self.ent_username = PlaceholderEntry(frame, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Username', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_username.grid(row=1, column=0, ipady=7.5)

        # ttk.Label(fr_text, text='Password').pack(anchor='w')
        self.ent_password = PlaceholderEntry(frame, 
                                             is_password=True, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password.grid(row=2, column=0, ipady=7.5)

        HyperlinkLabel(frame, 
                       text='Forgot Password?', 
                       on_click=lambda x: switch_to_window('forget_password'),
                       default_color='gray',
                       hover_color='black').grid(row=3, column=0, pady=0, sticky='w')

        self.btn_login = ttk.Button(frame, text='Login', padding=(87.5, 12.5), command=self.login)
        self.btn_login.grid(row=4, column=0, pady=10)

        back_button = ttk.Button(frame, text="Back", command=self.go_back)
        back_button.grid(row=5, column=0, pady=10, sticky='sw')

        frame.pack(padx=15, pady=15)
        
    def go_back(self):
        switch_to_window('landing')