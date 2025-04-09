import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from window_manager import switch_to_window
from sqlalchemy.orm import Session
import models
from models import Appointment, User, UserRole
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderText
from database import DatabaseManager

entry_font = ("Arial", 12)

class CreateAppointment(tk.Frame):
    def __init__(self, master, session, dbManager: DatabaseManager, current_user):
        super().__init__(master)
        self.session: Session = session
        self.current_user: User = current_user
        self.dbManager = dbManager

        frame = tk.Frame(self)
        frame.pack(padx=15, pady=15)

        # Title
        ttk.Label(frame, text="CREATE NEW APPOINTMENT", font=("Arial", 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Dropdown
        ttk.Label(frame, text="Select User:", font=entry_font).grid(row=1, column=0, sticky="w")
        self.patient_var = tk.StringVar()
        self.patient_dropdown = ttk.Combobox(frame, textvariable=self.patient_var, state="readonly", font=entry_font)
        
        # Replace with patients
        all_patients = self.dbManager.get_all_users() 
        all_patients = filter(lambda p: p.role == models.UserRole.PATIENT, all_patients)
        
        self.patient_user_dropdown_values = { }
        
        for p in all_patients:
            print(p.full_name)
            self.patient_user_dropdown_values[f"{p.full_name} (ID: {p.uuid})"] = p.uuid
        
        dropdown_keys = list(self.patient_user_dropdown_values.keys())
        self.patient_dropdown['values'] = dropdown_keys
        self.patient_dropdown.set(dropdown_keys[0])
        self.patient_dropdown.grid(row=2, column=0, sticky="ew", padx=(0, 10))

        if self.current_user.role == models.UserRole.PATIENT:
            self.patient_dropdown.set(f"{current_user.full_name} (ID: {current_user.uuid})")
            self.patient_dropdown.config(state="disabled")

        # Date Picker
        ttk.Label(frame, text="Date:", font=entry_font).grid(row=3, column=0, sticky="w")
        self.date_picker = DateEntry(frame, width=16, background='darkblue', foreground='white', borderwidth=2, font=entry_font, state="readonly")
        self.date_picker.set_date(datetime.date.today())
        self.date_picker.grid(row=4, column=0, sticky="ew", padx=(0, 10))

        # Time Picker
        ttk.Label(frame, text="Time (HH:MM):", font=entry_font).grid(row=5, column=0, sticky="w")

        time_frame = ttk.Frame(frame)
        time_frame.grid(row=6, column=0, sticky="w", padx=(0, 10))

        # Hour Spinbox
        self.hour_var = tk.StringVar()
        self.hour_spin = ttk.Spinbox(
        time_frame, from_=1, to=12, width=3, textvariable=self.hour_var, font=entry_font, wrap=True, justify='center', state='readonly'
        )
        self.hour_spin.set("01")
        self.hour_spin.grid(row=0, column=0, padx=(0, 5))

        # Minute Spinbox
        self.minute_var = tk.StringVar()
        self.minute_spin = ttk.Spinbox(
        time_frame, from_=0, to=59, width=3, textvariable=self.minute_var, font=entry_font, format="%02.0f", wrap=True, justify='center', state='readonly'
        )
        self.minute_spin.set("00")
        self.minute_spin.grid(row=0, column=1, padx=(0, 5))

        # AM/PM Combobox
        self.period_var = tk.StringVar()
        self.period_combo = ttk.Combobox(
        time_frame, textvariable=self.period_var, values=["AM", "PM"], width=4, state="readonly", font=entry_font, justify='center'
        )
        self.period_combo.set("AM")
        self.period_combo.grid(row=0, column=2)

        # Textbox for Reason using PlaceholderText
        ttk.Label(frame, text="Reason:", font=entry_font).grid(row=1, column=1, sticky="nw")
        self.reason_text = PlaceholderText(
            master=frame,
            placeholder_text="Write your reason here...",
            normal_font=entry_font,
            placeholder_font=entry_font,
            width=30,
            height=10
        )
        self.reason_text.grid(row=2, column=1, rowspan=5, sticky="nsew")

        # Submit Button
        self.submit_btn = ttk.Button(frame, text="Submit", command=self.submit_appointment, padding=(330, 12.5))
        self.submit_btn.grid(row=7, columnspan=2, pady=(50,10), sticky='ew')
        
        self.submit_btn = ttk.Button(frame, text="Back", command=self.goto_appointments, padding=(330, 12.5))
        self.submit_btn.grid(row=8, columnspan=2, pady=(0,10), sticky='ew')

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

    def submit_appointment(self):
        try:
            patient_id = self.patient_user_dropdown_values[self.patient_var.get()]
            
            date = self.date_picker.get_date()
            
            hour = int(self.hour_var.get()) + 12 if self.period_var.get() == "PM" else int(self.hour_var.get())
            time = datetime.time(hour, int(self.minute_var.get()))
            
            reason = self.reason_text.get_text().strip()
            if reason == "":
                showinfo("Alert", "Please input a reason.")
                return
            
            created_by_id = self.current_user.uuid

            date_time: datetime.datetime = datetime.datetime.combine(date=date, time=time)
            
            new_appointment = Appointment(
                patient_id,
                date_time,
                reason,
                created_by_id
            )

            self.session.add(new_appointment)
            self.session.commit()
            
            showinfo("Alert", "Appointment successfully created!")
            switch_to_window('appointments', onCreateArgs=(self.current_user, ))
        except Exception as e:
            self.session.rollback()
            print(f"Database error: {e}")
            showinfo("Error", "Unable to create appointment.")

    def goto_appointments(self):
        print(self.current_user)
        switch_to_window("appointments", onCreateArgs=(self.session, self.current_user))
        
