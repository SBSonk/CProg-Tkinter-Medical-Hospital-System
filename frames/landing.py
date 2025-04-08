import tkinter as tk
from tkinter import ttk
from tkinter import *
from window_manager import switch_to_window

class LandingFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


        # Title
        title_label = ttk.Label(self, text="Welcome to the Medical & Hospital System", font=("Arial", 16))
        title_label.pack(pady=20)

        # Login Button
        login_button = ttk.Button(self, text="Login", command=self.goto_login)
        login_button.pack(pady=10)

        # Register Button
        register_button = ttk.Button(self, text="Register", command=self.goto_register)
        register_button.pack(pady=10)

        # Sidebar Frame
        self.sidebar_frame = Frame(self, bg="#108cff", width=200, height=500)
        self.sidebar_frame.pack(side="left", fill="y")

        # Sidebar toggle button
        self.toggle_button = Button(self.sidebar_frame, text=">", bg="#034787", fg="white",
                                    cursor="hand2", font=("Arial", 16), relief="flat")
        self.toggle_button.pack(pady=10, padx=10, fill="x", anchor="w")

        # Main Content Frame
        self.content_frame = Frame(self, bg="#e73121", width=400, height=500)
        self.content_frame.pack(side="left", fill="both", expand=True)

    def goto_login(self):
        switch_to_window('login')

    def goto_register(self):
        switch_to_window('register')

