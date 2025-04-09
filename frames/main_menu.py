import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from window_manager import switch_to_window
import models
from models import UserRole

class MainMenu(tk.Frame):
    def __init__(self, master, session: Session, current_user: models.User):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        self.configure(width=400, height=540)
        self.pack_propagate(0)

        # Main container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label
        title_label = ttk.Label(container, text="Main Menu", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 30), anchor="center")

        # Button Frame
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=10)

        # Buttons with spacing
        buttons = []
        
        match current_user.role:
            case UserRole.ADMIN:
                buttons.append(("User Management", self.goto_register)) # MOVE TO User MANAGEMENT
                buttons.append(("Patient Management", self.goto_maintenance))
                buttons.append(("Appointment System", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_appointments)) # move to notes
            case UserRole.DOCTOR: 
                buttons.append(("Patient Management", self.goto_maintenance))
                buttons.append(("Appointment System", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_appointments)) # move to notes
            case UserRole.NURSE:
                buttons.append(("Patient Management", self.goto_maintenance))
                buttons.append(("Appointment System", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_appointments)) # move to notes
            case UserRole.PATIENT:
                buttons.append(("My Appointments", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_appointments))

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, padding=(87.5, 12.5))
            btn.pack(fill="x", pady=8)

        # Spacer
        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=20)

        # Logout at bottom
        logout_button = ttk.Button(container, text="Logout")
        logout_button.pack(pady=(0, 10), anchor="e")

    def goto_appointments(self):
        print(self.current_user)
        if self.current_user.role == models.UserRole.PATIENT:
            switch_to_window("appointment_patient", onCreateArgs=(self.session, self.current_user))
        elif self.current_user.role == models.UserRole.NURSE:
            switch_to_window("appointment_nurse", onCreateArgs=(self.session, self.current_user))

    def goto_maintenance(self):
        print(self.current_user)
        if self.current_user.role == models.UserRole.ADMIN:
            switch_to_window("record_maintenance_menu", onCreateArgs=(self.session, self.current_user))

    def goto_register(self):
        switch_to_window('register')
        
            
