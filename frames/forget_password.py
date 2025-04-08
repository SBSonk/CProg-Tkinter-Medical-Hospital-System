import tkinter as tk
import models
from sqlalchemy.orm import Session
from sqlalchemy import Select
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window
from database import DatabaseManager

class ForgetPassword(tk.Frame):
    ent_username: tk.Entry = None
    btn_next: tk.Button = None
    dbManager: DatabaseManager = None

    def submitUsername(self):
        try:
            user = self.dbManager.get_user_by_username(self.ent_username.get())

            if user:
                switch_to_window('reset_password', onCreateArgs=(user,))
            else:
                print('User does not exist.')
        except Exception as e:
            print(f"Database Error: {e}")

    def __init__(self, master, dbManager):
        super().__init__(master)
        self.dbManager = dbManager

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0)
        frame.grid_rowconfigure(1, pad=20)
        frame.grid_rowconfigure(2, pad=20)
        ttk.Label(frame, text='Reset Password', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)
        
        self.ent_username = PlaceholderEntry(frame, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Username', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_username.grid(row=1, column=0, ipady=7.5)

        HyperlinkLabel(frame, 
                       text='Return to login', 
                       on_click=lambda x: switch_to_window('login'),
                       default_color='gray',
                       hover_color='black').grid(row=3, column=0, pady=0, sticky='w')

        self.btn_next = ttk.Button(frame, text='Next', padding=(87.5, 12.5), command=self.submitUsername)
        self.btn_next.grid(row=4, column=0, pady=10)

        frame.pack(padx=15, pady=15)
        

    