import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from models import Appointment, User, UserRole
from datetime import datetime
from window_manager import switch_to_window

class AppointmentPatient(tk.Frame):
    def __init__(self, master, session: Session, current_user):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        self.pack(fill="both", expand=True)

        ttk.Label(self, text="My Appointments", font=("Arial", 16)).pack(pady=10)

        #ttk.Button(self, text="Reschedule Selected Appointment", command=self.reschedule_appointment).pack(pady=10)
        ttk.Button(self, text="Schedule New Appointment", command=lambda: switch_to_window("create_appointment", onCreateArgs=(current_user,))).pack(pady=10)

        self.appointment_tree = ttk.Treeview(self, columns=("Date", "Reason"), show="headings")
        self.appointment_tree.heading("Date", text="Scheduled Time")
        self.appointment_tree.heading("Reason", text="Reason")
        self.appointment_tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.LoadTable()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        #ttk.Button(button_frame, text="New Appointment", command=self.new_appointment).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Reschedule Selected Appointment", command=self.reschedule_appointment).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Cancel Selected Appointment", command=self.cancel_appointment).grid(row=0, column=2, padx=5)
        ttk.Button(self, text="Back", command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).pack(pady=10)

    def LoadTable(self):
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
            
        appointments = self.session.query(Appointment).filter_by(patient_id=self.current_user.uuid).all()
        
        if self.current_user.role == UserRole.PATIENT:
            appointments = filter(lambda n: n.patient_id == self.current_user.uuid, appointments)

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
        self.LoadTable()
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
                self.LoadTable()
                win.destroy()
                messagebox.showinfo("Success", f"Appointment {'updated' if appointment else 'created'} successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Save", command=save).pack(pady=10)
