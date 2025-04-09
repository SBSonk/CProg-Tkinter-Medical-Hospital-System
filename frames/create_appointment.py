import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from window_manager import switch_to_window
from sqlalchemy.orm import Session
from models import Appointment, User
from tkinter.messagebox import showinfo

entry_font = ("Arial", 12)

class CreateAppointment(tk.Frame):
    def __init__(self, master, session, current_user):
        super().__init__(master)
        self.session: Session = session
        self.current_user: User = current_user

        frame = tk.Frame(self)
        frame.pack(padx=15, pady=15)

        # Title
        ttk.Label(frame, text="CREATE NEW APPOINTMENT", font=("Arial", 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Dropdown
        ttk.Label(frame, text="Select User:", font=entry_font).grid(row=1, column=0, sticky="w")
        self.patient_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(frame, textvariable=self.patient_var, state="readonly", font=entry_font)
        
        # Replace with users
        self.user_dropdown_values = {
            "Pablo": 3,
        }
        dropdown_keys = list(self.user_dropdown_values.keys())
        self.type_dropdown['values'] = dropdown_keys
        self.type_dropdown.set(dropdown_keys[0])
        self.type_dropdown.grid(row=2, column=0, sticky="ew", padx=(0, 10))

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

        # Textbox for Reason
        ttk.Label(frame, text="Reason:", font=entry_font).grid(row=1, column=1, sticky="nw")
        self.reason_text = tk.Text(frame, width=30, height=10, font=entry_font)
        self.reason_text.grid(row=2, column=1, rowspan=5, sticky="nsew")

        # Submit Button
        self.submit_btn = ttk.Button(frame, text="Submit", command=self.submit_appointment, padding=(330, 12.5))
        self.submit_btn.grid(row=7, columnspan=2, pady=(50,10), sticky='ew')

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

    def submit_appointment(self):
        try:
            patient_id = self.user_dropdown_values[self.patient_var.get()]
            
            date = self.date_picker.get_date()
            
            hour = int(self.hour_var.get()) + 12 if self.period_var.get() == "PM" else int(self.hour_var.get())
            time = datetime.time(hour, int(self.minute_var.get()))
            
            reason = self.reason_text.get("1.0", "end").strip()
            if reason == "":
                showinfo("Alert", "Please input a reason.")
                return
            
            created_by_id = self.current_user.uuid

            date_time: datetime.datetime = datetime.datetime.combine(date=date, time=time)


            print(f"User_id: {patient_id}")
            print(f"Date_time: {date_time}")
            print(f"Reason: {reason}")
            print(f"Created_by_id: {created_by_id}")

            new_appointment = Appointment(
                patient_id,
                date_time,
                reason,
                created_by_id
            )

            self.session.add(new_appointment)
            self.session.commit()
            
            showinfo("Alert", "Appointment successfully created!")
        except Exception as e:
            print(f"Database error: {e}")
            showinfo("Error", "Unable to create appointment.")

    def go_back(self):
        switch_to_window('landing')
