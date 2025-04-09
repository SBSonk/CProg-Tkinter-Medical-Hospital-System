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
    note_to_edit: models.DoctorNote = None
    
    def __init__(self, master, session, dbManager: DatabaseManager, current_user, note_to_edit: models.DoctorNote = None):
        super().__init__(master)
        self.session: Session = session
        self.current_user: User = current_user
        self.dbManager = dbManager

        frame = tk.Frame(self)
        frame.pack(padx=15, pady=15)

        # Title
        if not note_to_edit:
            ttk.Label(frame, text="CREATE DOCTOR'S NOTE", font=("Arial", 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        else:
            ttk.Label(frame, text="EDIT DOCTOR'S NOTE", font=("Arial", 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))
            
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
            print(p.full_name)
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
        save_text = "Create Note" if not note_to_edit else "Save Changes"
        self.submit_btn = ttk.Button(frame, text=save_text, command=self.submit_note, padding=(330, 12.5))
        self.submit_btn.grid(row=7, columnspan=2, pady=(50,10), sticky='ew')

        self.back_btn = ttk.Button(frame, text="Back", command=self.go_to_doctors_notes, padding=(330, 12.5))
        self.back_btn.grid(row=8, columnspan=2, pady=(0,10), sticky='ew')

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        
        # Set original values if editing
        if note_to_edit:
            original_patient = dbManager.get_user(note_to_edit.patient_id)
            self.patient_dropdown.set(f"{original_patient.full_name} (ID: {original_patient.uuid})")
            self.patient_dropdown.configure(state="disabled")
            self.note_text.set_text(note_to_edit.note)
            
            self.note_to_edit = note_to_edit

    def submit_note(self):
        try:
            patient_id = self.patient_user_dropdown_values[self.patient_var.get()]
            note = self.note_text.get_text().strip()
            if note == "":
                showinfo("Alert", "Please input a reason.")
                return
            
            created_by_id = self.current_user.uuid
            
            if self.note_to_edit:
                self.note_to_edit.note = note
                self.session.commit()
                showinfo("Alert", "Doctor note successfully updated!")
            else:
                new_note = DoctorNote(
                    patient_id,
                    note,
                    created_by_id
                )

                self.session.add(new_note)
                self.session.commit()
                
                showinfo("Alert", "Doctor note successfully created!")
            switch_to_window('doctors_notes', onCreateArgs=(self.current_user,))
        except Exception as e:
            self.session.rollback()
            print(f"Database error: {e}")
            showinfo("Error", "Unable to create doctor note.")

    def go_to_doctors_notes(self):
        switch_to_window("doctors_notes", onCreateArgs=(self.current_user,))
