import tkinter as tk
import models
from sqlalchemy.orm import Session
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

class MainMenu(tk.Frame):
    ent_username: tk.Entry = None
    ent_password: tk.Entry = None

    def __init__(self, master):
        super().__init__(master)

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0)
        frame.grid_rowconfigure(1, pad=20)
        frame.grid_rowconfigure(2, pad=20)
        ttk.Label(frame, text='Main Menu', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)

        frame.pack()