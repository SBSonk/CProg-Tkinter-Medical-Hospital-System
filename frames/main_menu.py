import tkinter as tk
from tkinter import ttk
from window_manager import switch_to_window
import models

class MainMenu(tk.Frame):
    def __init__(self, master, current_user):
        super().__init__(master)
        self.current_user = current_user["user"]

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0)
        frame.grid_rowconfigure(1, pad=20)
        frame.grid_rowconfigure(2, pad=20)

        ttk.Label(frame, text='Main Menu', font=('Arial', 24)).grid(row=0, column=0, sticky='w', pady=10)

        appointment_button = ttk.Button(
            frame,
            text="Appointment System",
            command=self.goto_appointments
        )
        appointment_button.grid(row=1, column=0, sticky="w")

        frame.pack()

    def goto_appointments(self):
        if self.current_user.role == models.UserRole.PATIENT:
            switch_to_window("patient_appointments")
        elif self.current_user.role == models.UserRole.NURSE:
            switch_to_window("nurse_appointments")
