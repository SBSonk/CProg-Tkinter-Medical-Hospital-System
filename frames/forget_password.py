import tkinter as tk
import models
from sqlalchemy.orm import Session
from sqlalchemy import Select
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window


class ForgetPassword(tk.Frame):
    ent_email: tk.Entry = None
    btn_next: tk.Button = None

    login_success = None
    login_fail = None

    session: Session = None

    def login(self):
        statement = Select(models.User).where(models.User.username == self.ent_username.get())
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

    def __init__(self, master):
        super().__init__(master)

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0)
        frame.grid_rowconfigure(1, pad=20)
        frame.grid_rowconfigure(2, pad=20)
        ttk.Label(frame, text='Reset Password', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)

        # ttk.Label(fr_text, text='Username').pack(anchor='w')
        self.ent_email = PlaceholderEntry(frame, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Username', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_email.grid(row=1, column=0, ipady=7.5)

        HyperlinkLabel(frame, 
                       text='Return to login', 
                       on_click=lambda x: switch_to_window('register'),
                       default_color='gray',
                       hover_color='black').grid(row=3, column=0, pady=0, sticky='w')

        self.btn_next = ttk.Button(frame, text='Next', padding=(87.5, 12.5), command=self.login)
        self.btn_next.grid(row=4, column=0, pady=10)

        frame.pack()