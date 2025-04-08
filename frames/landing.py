import tkinter as tk
import models
from sqlalchemy.orm import Session
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

class LandingFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(padx=50, pady=50)

        # Title
        title_label = ttk.Label(self, text="Welcome to the Medical & Hospital System", font=("Arial", 16))
        title_label.pack(pady=20)

        # Login Button
        login_button = ttk.Button(self, text="Login", command=self.goto_login)
        login_button.pack(pady=10)

        # ✅ Register Button
        register_button = ttk.Button(self, text="Register", command=self.goto_register)
        register_button.pack(pady=10)

    def goto_login(self):
        switch_to_window('login')

    # ✅ This is the new method for register button
    def goto_register(self):
        switch_to_window('register')