import tkinter as tk
import models
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from models import Appointment, User, UserRole
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

        #ttk.Button(form_frame, text="Schedule Appointment", command=self.schedule_appointment).grid(row=2, columnspan=2, pady=10)
        #ttk.Button(self, text="Reschedule Selected Appointment", command=self.reschedule_appointment).pack(pady=10)
        ttk.Button(self, text="Schedule New Appointment", command=lambda: switch_to_window("create_appointment", onCreateArgs=(current_user,))).pack(pady=10)

        self.appointments_tree = ttk.Treeview(self, columns=("id", "datetime", "reason", "patient"), show="headings")
        self.appointments_tree.heading("id", text="ID")
        self.appointments_tree.heading("datetime", text="Date/Time")
        self.appointments_tree.heading("reason", text="Reason")
        self.appointments_tree.heading("patient", text="Patient")
        self.appointments_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        action_frame = ttk.Frame(self)
        action_frame.pack(pady=10)

        
        ttk.Button(action_frame, text="Reschedule Selected Appointment", command=self.reschedule_appointment).grid(row=0, column=1, padx=5)

        ttk.Button(action_frame, text="Cancel Selected Appointment", command=self.cancel_appointment).grid(row=0, column=2, padx=5)

        ttk.Button(self, text="Back", command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).pack(pady=10)

        self.load_appointments()

    def load_appointments(self):
        for row in self.appointments_tree.get_children():
            self.appointments_tree.delete(row)

        if self.current_user.role == UserRole.NURSE:
            appointments = self.session.query(Appointment).all()
        else:
            appointments = self.session.query(Appointment).filter_by(patient_id=self.current_user.uuid).all()

        for appt in appointments:
            patient = self.session.query(User).filter_by(uuid=appt.patient_id).first()
            self.appointments_tree.insert("", "end", values=(patient.uuid, appt.scheduled_time.strftime("%Y-%m-%d %H:%M"), appt.reason, patient.full_name))

    def refresh_appointments(self):
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)

        appointments = self.session.query(Appointment).filter_by(patient_id=self.current_user.uuid).all()
        for appt in appointments:
            self.appointments_tree.insert("", "end", iid=appt.id, values=(appt.scheduled_time, appt.reason))
    
    def schedule_appointment(self):
        reason = self.reason_entry.get()
        dt_str = self.datetime_entry.get()

        try:
            scheduled_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date", "Enter datetime as YYYY-MM-DD HH:MM")
            return

        new_appointment = Appointment(
            patient_id=self.current_user.uuid,
            scheduled_time=scheduled_time,
            reason=reason,
            created_by_id=self.current_user.uuid,
        )

        self.session.add(new_appointment)
        self.session.commit()
        self.load_appointments()
        self.reason_entry.delete(0, tk.END)
        self.datetime_entry.delete(0, tk.END)

    def reschedule_appointment(self):
        selected = self.appointments_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment to reschedule.")
            return
        appt_id = self.appointments_tree.item(selected)['values'][0]
        appt = self.session.query(Appointment).filter_by(id=appt_id).first()
        self._open_appointment_window("Reschedule Appointment", appt)

    def cancel_appointment(self):
        selected = self.appointments_tree.focus()
        if not selected:
            messagebox.showinfo("No selection", "Select an appointment to cancel")
            return

        appt_id = self.appointments_tree.item(selected)['values'][0]
        appt = self.session.query(Appointment).filter_by(id=appt_id).first()

        # if self.current_user.role != models.UserRole.NURSE and appt.patient_id != self.current_user.uuid:
        #     messagebox.showerror("Unauthorized", "You can only cancel your own appointments")
        #     return

        self.session.delete(appt)
        self.session.commit()
        self.load_appointments()

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
                        patient_id=self.current_user.uuid,
                        scheduled_time=time,
                        reason=reason,
                        created_by_id=self.current_user.uuid
                    )
                    self.session.add(new_appt)
                self.session.commit()
                self.refresh_appointments()
                win.destroy()
                messagebox.showinfo("Success", f"Appointment {'updated' if appointment else 'created'} successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Save", command=save).pack(pady=10)

