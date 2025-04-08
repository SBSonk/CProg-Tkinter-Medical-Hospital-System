import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from models import Appointment, User
from datetime import datetime
from window_manager import switch_to_window

class AppointmentNurse(tk.Frame):
    def __init__(self, master, session: Session, current_user: User):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        self.appointments_tree = None
        self.reason_entry = None
        self.datetime_entry = None

        ttk.Label(self, text="Appointment Scheduler", font=("Arial", 20)).pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Reason:").grid(row=0, column=0, padx=5, pady=5)
        self.reason_entry = ttk.Entry(form_frame)
        self.reason_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="DateTime (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=5, pady=5)
        self.datetime_entry = ttk.Entry(form_frame)
        self.datetime_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Schedule Appointment", command=self.schedule_appointment).grid(row=2, columnspan=2, pady=10)

        self.appointments_tree = ttk.Treeview(self, columns=("id", "datetime", "reason", "patient"), show="headings")
        self.appointments_tree.heading("id", text="ID")
        self.appointments_tree.heading("datetime", text="Date/Time")
        self.appointments_tree.heading("reason", text="Reason")
        self.appointments_tree.heading("patient", text="Patient")
        self.appointments_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        action_frame = ttk.Frame(self)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Reschedule", command=self.reschedule_appointment).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Cancel", command=self.cancel_appointment).grid(row=0, column=1, padx=5)

        ttk.Button(self, text="Back", command=lambda: switch_to_window("main_menu", self.current_user)).pack(pady=10)

        self.load_appointments()

    def load_appointments(self):
        for row in self.appointments_tree.get_children():
            self.appointments_tree.delete(row)

        if self.current_user.user_type == "nurse":
            appointments = self.session.query(Appointment).all()
        else:
            appointments = self.session.query(Appointment).filter_by(patient_id=self.current_user.id).all()

        for appt in appointments:
            patient_name = self.session.query(User).filter_by(id=appt.patient_id).first().username
            self.appointments_tree.insert("", "end", values=(appt.id, appt.scheduled_time.strftime("%Y-%m-%d %H:%M"), appt.reason, patient_name))

    def schedule_appointment(self):
        reason = self.reason_entry.get()
        dt_str = self.datetime_entry.get()

        try:
            scheduled_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date", "Enter datetime as YYYY-MM-DD HH:MM")
            return

        new_appointment = Appointment(
            patient_id=self.current_user.id,
            scheduled_time=scheduled_time,
            reason=reason,
            created_by_id=self.current_user.id,
        )

        self.session.add(new_appointment)
        self.session.commit()
        self.load_appointments()
        self.reason_entry.delete(0, tk.END)
        self.datetime_entry.delete(0, tk.END)

    def reschedule_appointment(self):
        selected = self.appointments_tree.focus()
        if not selected:
            messagebox.showinfo("No selection", "Select an appointment to reschedule")
            return

        appt_id = self.appointments_tree.item(selected)['values'][0]
        dt_str = self.datetime_entry.get()

        try:
            new_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date", "Enter datetime as YYYY-MM-DD HH:MM")
            return

        appt = self.session.query(Appointment).filter_by(id=appt_id).first()
        if self.current_user.user_type != "nurse" and appt.patient_id != self.current_user.id:
            messagebox.showerror("Unauthorized", "You can only reschedule your own appointments")
            return

        appt.scheduled_time = new_time
        self.session.commit()
        self.load_appointments()

    def cancel_appointment(self):
        selected = self.appointments_tree.focus()
        if not selected:
            messagebox.showinfo("No selection", "Select an appointment to cancel")
            return

        appt_id = self.appointments_tree.item(selected)['values'][0]
        appt = self.session.query(Appointment).filter_by(id=appt_id).first()

        if self.current_user.user_type != "nurse" and appt.patient_id != self.current_user.id:
            messagebox.showerror("Unauthorized", "You can only cancel your own appointments")
            return

        self.session.delete(appt)
        self.session.commit()
        self.load_appointments()
