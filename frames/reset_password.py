import tkinter as tk
import models
from sqlalchemy.orm import Session
from sqlalchemy import Select
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

class ResetPassword(tk.Frame):
    ent_password: tk.Entry = None
    ent_password_confirm: tk.Entry = None
    lbl_greeting: ttk.Label = None
    btn_next: tk.Button = None

    user_to_edit: models.User = None

    def submitPassword(self):
        print(self.user_to_edit)

    def __init__(self, master, user_to_edit: models.User):
        super().__init__(master)
        self.user_to_edit = user_to_edit

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0)
        frame.grid_rowconfigure(1, pad=20)
        frame.grid_rowconfigure(2, pad=20)
        self.lbl_greeting = ttk.Label(frame, text=f'Reset password for: {user_to_edit.full_name}', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)
        
        self.ent_password = PlaceholderEntry(frame, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Enter Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password.grid(row=1, column=0, ipady=7.5)

        self.ent_password_confirm = PlaceholderEntry(frame, 
                                             is_password=False, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Confirm Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password_confirm.grid(row=2, column=0, ipady=7.5)

        self.btn_next = ttk.Button(frame, text='Next', padding=(87.5, 12.5))
        self.btn_next.grid(row=4, column=0, pady=10)

        frame.pack(padx=15, pady=15)