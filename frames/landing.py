import tkinter as tk
from tkinter import ttk
from tkinter import *
from window_manager import switch_to_window

class LandingFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        frame = tk.Frame(self)
        frame.pack(padx=15, pady=15)
        
        # Title
        title_label = ttk.Label(frame, text="Welcome to the Medical & Hospital System", font=("Arial", 24))
        title_label.pack(pady=20)

        # Login Button
        login_button = ttk.Button(frame, text="Login", command=self.goto_login)
        login_button.pack(pady=10, ipadx=40, ipady=20)

    def goto_login(self):
        switch_to_window('login')

