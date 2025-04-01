import tkinter as tk
import models
from sqlalchemy.orm import Session
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

class Register(tk.Frame):
    ent_username: tk.Entry = None
    ent_password: tk.Entry = None
    btn_login: tk.Button = None

    session = None

    def register_account(self):
        # todo: validate contents

        new_user = models.User(
            username = self.ent_username.get(),
            password = self.ent_password.get()
        )

        print(new_user)

        try:
            self.session.add(new_user)
            self.session.commit()
            print('User creation success.')
            showinfo('Alert', 'User successfully created!')
        except Exception as e:
            print('User creation failed.')
            print(e)
            showinfo('Alert', 'User successfully failed!')

    def __init__(self, master, session: Session):
        super().__init__(master)
        self.session = session

        fr_text = tk.Frame(self, width=384, height=540)
        fr_text.grid_rowconfigure(0)
        fr_text.grid_rowconfigure(1, pad=20)
        fr_text.grid_rowconfigure(2, pad=20)
        ttk.Label(fr_text, text='Register', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)

        # ttk.Label(fr_text, text='Username').pack(anchor='w')
        self.ent_username = PlaceholderEntry(fr_text, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Username', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_username.grid(row=1, column=0, ipady=7.5)

        # ttk.Label(fr_text, text='Password').pack(anchor='w')
        self.ent_password = PlaceholderEntry(fr_text, 
                                             is_password=True, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password.grid(row=2, column=0, ipady=7.5)

        HyperlinkLabel(fr_text, 
                       text='Login', 
                       on_click=lambda x: switch_to_window('login'),
                       default_color='gray',
                       hover_color='black').grid(row=3, column=0, pady=0, sticky='w')

        self.btn_register = ttk.Button(fr_text, text='Create Account', padding=(80, 12.5), command=self.register_account)
        self.btn_register.grid(row=4, column=0, pady=10)

        fr_text.pack()