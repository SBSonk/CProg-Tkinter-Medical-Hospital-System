import tkinter as tk
import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from custom_widgets import HyperlinkLabel
from window_manager import switch_to_window

class Login(tk.Frame):
    ent_username: tk.Entry = None
    ent_password: tk.Entry = None
    btn_login: tk.Button = None

    login_success = None
    login_fail = None

    session: Session = None

    def login(self):
        statement = select(models.User).where(models.User.username == self.ent_username.get())
        user: models.User = self.session.execute(statement).scalar_one_or_none()
        
        if not user:
            print('User does not exist.')
            return
        
        if user.check_password(self.ent_password.get()):
            print('Logged in successfully.')
            if callable(self.login_success):
                self.login_success()
        else:
            print('Incorrect password.')
            if callable(self.login_fail):
                self.login_fail()

    def __init__(self, master, session: Session, login_success = None, login_fail = None):
        super().__init__(master)
        self.session = session

        self.login_success = login_success
        self.login_fail = login_fail

        fr_text = tk.Frame(self, padx=60, pady=15)
        tk.Label(fr_text, text='LOGIN', font=('Arial', 24)).pack(pady=(0, 20))

        tk.Label(fr_text, text='Username').pack(anchor='w')
        self.ent_username = tk.Entry(fr_text)
        self.ent_username.pack(pady=(0, 10))

        tk.Label(fr_text, text='Password').pack(anchor='w', pady=(10, 0))
        self.ent_password = tk.Entry(fr_text, show='*')
        self.ent_password.pack()

        HyperlinkLabel(fr_text, 
                            text='Register', 
                            on_click=lambda x: switch_to_window('register'),
                            default_color='gray',
                            hover_color='black').pack(pady=(20, 0))

        self.btn_login = tk.Button(fr_text, text='Login', padx=50, pady=10, command=self.login)
        self.btn_login.pack(pady=(20, 0))
        
        fr_text.pack()
        

    