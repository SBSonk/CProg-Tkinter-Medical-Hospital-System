import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from window_manager import switch_to_window
from sqlalchemy.orm import Session
import models
from models import DoctorNote, User, UserRole
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderText
from database import DatabaseManager

entry_font = ("Arial", 12)

class CreateDoctorNote(tk.Frame):
    def __init__(self, master, session, dbManager: DatabaseManager, current_user):
        super().__init__(master)
        self.session: Session = session
        self.current_user: User = current_user
        self.dbManager = dbManager

        frame = tk.Frame(self)
        frame.pack(padx=15, pady=15)

        # Title
        ttk.Label(frame, text="CREATE DOCTOR'S NOTE", font=("Arial", 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Patient Dropdown Label
        ttk.Label(frame, text="PATIENT NAME", font=entry_font).grid(row=1, column=0, sticky='w', padx=5)

        # Dropdown (Combobox)
        self.patient_var = tk.StringVar()
        self.patient_dropdown = ttk.Combobox(frame, textvariable=self.patient_var, state="readonly", width=40, font=entry_font)
        self.patient_dropdown.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20), padx=5)

        # Populate patient dropdown 
        all_patients = self.dbManager.get_all_users() 
        all_patients = filter(lambda p: p.role == models.UserRole.PATIENT, all_patients)
        
        self.patient_user_dropdown_values = { }
        
        for p in all_patients:
            self.patient_user_dropdown_values[f"{p.full_name} (ID: {p.uuid})"] = p.uuid
        
        dropdown_keys = list(self.patient_user_dropdown_values.keys())
        self.patient_dropdown['values'] = dropdown_keys
        self.patient_dropdown.set(dropdown_keys[0])
        
        # Note Text Box
        self.note_text = PlaceholderText(
            master=frame,
            placeholder_text="Write your note here...",
            normal_font=entry_font,
            placeholder_font=entry_font,
            width=30,
            height=10
        )
        self.note_text.grid(row=3, column=0, columnspan=2, pady=(0, 20), padx=5)

        # Submit Button
        self.submit_btn = ttk.Button(frame, text="Submit", command=self.submit_note, padding=(330, 12.5))
        self.submit_btn.grid(row=7, columnspan=2, pady=(50,10), sticky='ew')

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

    def submit_note(self):
        try:
            patient_id = self.patient_user_dropdown_values[self.patient_var.get()]
            note = self.note_text.get_text().strip()
            if note == "":
                showinfo("Alert", "Please input a reason.")
                return
            
            created_by_id = self.current_user.uuid
            
            new_note = DoctorNote(
                patient_id,
                note,
                created_by_id
            )

            self.session.add(new_note)
            self.session.commit()
            
            showinfo("Alert", "Doctor note successfully created!")
        except Exception as e:
            self.session.rollback()
            print(f"Database error: {e}")
            showinfo("Error", "Unable to create doctor note.")

    def goto_appointments(self):
        print(self.current_user)
        if self.current_user.role == models.UserRole.PATIENT:
            switch_to_window("appointment_patient", onCreateArgs=(self.session, self.current_user))
        elif self.current_user.role == models.UserRole.NURSE:
            switch_to_window("appointment_nurse", onCreateArgs=(self.session, self.current_user))
