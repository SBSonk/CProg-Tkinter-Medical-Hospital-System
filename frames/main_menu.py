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
                buttons.append(("User Management", self.goto_user_management))
                buttons.append(("Patient List", self.goto_patient_list))
                buttons.append(("Appointment System", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_doctor_notes))
            case UserRole.DOCTOR:
                buttons.append(("Patient List", self.goto_patient_list))
                buttons.append(("Appointment System", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_doctor_notes))
            case UserRole.NURSE:
                buttons.append(("Patient List", self.goto_patient_list))
                buttons.append(("Appointment System", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_doctor_notes))
            case UserRole.PATIENT:
                buttons.append(("My Appointments", self.goto_appointments))
                buttons.append(("Doctor's Notes", self.goto_doctor_notes))

        buttons.append(("Logout", self.logout))

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, padding=(87.5, 12.5))
            btn.pack(fill="x", pady=8)

        # Divider
        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=20)

        # User info display
        info_frame = ttk.Frame(container)
        info_frame.pack(pady=10, fill="x")

        ttk.Label(info_frame, text="Your Information", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))

        user_info = {
            "Full Name": current_user.full_name or "N/A",
            "Age": current_user.age if current_user.age is not None else "N/A",
            "Gender": current_user.gender or "N/A",
            "Contact Info": current_user.contact_info or "N/A"
        }

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=20)

        for key, value in user_info.items():
            line = f"{key}: {value}"
            ttk.Label(info_frame, text=line, font=("Arial", 12)).pack(anchor="w", pady=2)

        # Spacer to push logout button down
        ttk.Frame(container).pack(expand=True)

        # Logout button at bottom right
        logout_button = ttk.Button(container, text="Logout", command=self.logout)
        logout_button.pack(anchor="e", pady=(0, 10))

    def goto_appointments(self):
        switch_to_window("appointments", onCreateArgs=(self.current_user,))

    def goto_user_management(self):
        switch_to_window("user_account_module", onCreateArgs=(self.current_user,))

    def goto_patient_list(self):
        switch_to_window("patient_info_module", onCreateArgs=(self.current_user,))
        
    def goto_doctor_notes(self):
        switch_to_window("doctors_notes", onCreateArgs=(self.current_user,))

    def goto_maintenance(self):
        if self.current_user.role == models.UserRole.ADMIN:
            switch_to_window("record_maintenance_menu", onCreateArgs=(self.current_user,))

    def goto_register(self):
        switch_to_window("register")

    def logout(self):
        switch_to_window("login")