import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from datetime import datetime
from models import Appointment

class AppointmentPatient(tk.Frame):
    def __init__(self, master, session: Session, current_user):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        self.pack(fill="both", expand=True)

        ttk.Label(self, text="My Appointments", font=("Arial", 16)).pack(pady=10)

        self.appointment_tree = ttk.Treeview(self, columns=("Date", "Reason"), show="headings")
        self.appointment_tree.heading("Date", text="Scheduled Time")
        self.appointment_tree.heading("Reason", text="Reason")
        self.appointment_tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_appointments()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="New Appointment", command=self.new_appointment).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Reschedule", command=self.reschedule_appointment).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_appointment).grid(row=0, column=2, padx=5)

    def refresh_appointments(self):
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        appointments = self.session.query(Appointment).filter_by(patient_id=self.current_user.id).all()
        for appt in appointments:
            self.appointment_tree.insert("", "end", iid=appt.id, values=(appt.scheduled_time, appt.reason))

    def new_appointment(self):
        self._open_appointment_window("Create Appointment")

    def reschedule_appointment(self):
        selected = self.appointment_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment to reschedule.")
            return
        appt_id = int(selected[0])
        appt = self.session.query(Appointment).get(appt_id)
        self._open_appointment_window("Reschedule Appointment", appt)

    def cancel_appointment(self):
        selected = self.appointment_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment to cancel.")
            return
        appt_id = int(selected[0])
        self.session.query(Appointment).filter_by(id=appt_id).delete()
        self.session.commit()
        self.refresh_appointments()
        messagebox.showinfo("Success", "Appointment canceled.")

    def _open_appointment_window(self, title, appointment=None):
        win = tk.Toplevel(self)
        win.title(title)

        ttk.Label(win, text="Date & Time (YYYY-MM-DD HH:MM):").pack(pady=5)
        entry_time = ttk.Entry(win)
        entry_time.pack(pady=5)

        ttk.Label(win, text="Reason").pack(pady=5)
        entry_reason = ttk.Entry(win)
        entry_reason.pack(pady=5)

        if appointment:
            entry_time.insert(0, appointment.scheduled_time.strftime("%Y-%m-%d %H:%M"))
            entry_reason.insert(0, appointment.reason)

        def save():
            try:
                time = datetime.strptime(entry_time.get(), "%Y-%m-%d %H:%M")
                reason = entry_reason.get()
                if appointment:
                    appointment.scheduled_time = time
                    appointment.reason = reason
                else:
                    new_appt = Appointment(
                        patient_id=self.current_user.id,
                        scheduled_time=time,
                        reason=reason,
                        created_by_id=self.current_user.id
                    )
                    self.session.add(new_appt)
                self.session.commit()
                self.refresh_appointments()
                win.destroy()
                messagebox.showinfo("Success", f"Appointment {'updated' if appointment else 'created'} successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Save", command=save).pack(pady=10)
