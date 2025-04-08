import tkinter as tk
from tkinter import ttk

class LandingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Label
        title_label = ttk.Label(self, text="Welcome to the Medical & Hospital System", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=40)

        # Login Button
        login_button = ttk.Button(self, text="Login", command=lambda: controller.show_frame(controller.frames['LoginFrame'].__class__))
        login_button.pack(pady=10, ipadx=10, ipady=5)

        # Register Button
        register_button = ttk.Button(self, text="Register", command=lambda: controller.show_frame(controller.frames['RegisterFrame'].__class__))
        register_button.pack(pady=10, ipadx=10, ipady=5)