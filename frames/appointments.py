import tkinter as tk
import models
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from models import Appointment, User, UserRole
from datetime import datetime
from window_manager import switch_to_window
from tkinter.messagebox import showinfo

class Appointments(tk.Frame):
    def __init__(self, master, session: Session, current_user: User):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        self.appointments_tree = None
        self.reason_entry = None
        self.datetime_entry = None

        frame = ttk.Frame(self)
        frame.pack(padx=15, pady=15)

        ttk.Label(frame, text="Appointment System", font=("Arial", 24, 'bold')).pack(pady=10)
        
        # Treeview to display appointments
        self.appointments_tree = ttk.Treeview(frame, columns=("id", "datetime", "reason", "patient", "status"), show="headings")
        self.appointments_tree.heading("id", text="ID")
        self.appointments_tree.heading("datetime", text="Date/Time")
        self.appointments_tree.heading("reason", text="Reason")
        self.appointments_tree.heading("patient", text="Patient")
        self.appointments_tree.heading("status", text="Status")
        self.appointments_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame for the action buttons
        button_frame = tk.Frame(frame)
        button_frame.pack()
        buttons = [
            ttk.Button(button_frame, text="Schedule New Appointment", command=lambda: switch_to_window("create_appointment", onCreateArgs=(current_user,))),
            ttk.Button(button_frame, text="Reschedule Selected Appointment", command=self.EditAppointment),
            ttk.Button(button_frame, text="Cancel Selected Appointment", command=self.CancelAppointment)
        ]

        i = 0
        for b in buttons:
            b.grid(row=0, column=i)
            i += 1
        
        # Button to go back to the main menu
        ttk.Button(frame, text="Back to Main Menu", width=30,
                   command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).pack(pady=20)
                
        # Load appointments into the table
        self.LoadTable()


    def LoadTable(self):
        for row in self.appointments_tree.get_children():
            self.appointments_tree.delete(row)

        if self.current_user.role != UserRole.PATIENT:
            appointments = self.session.query(Appointment).all()
        else:
            appointments = self.session.query(Appointment).filter_by(patient_id=self.current_user.uuid).all()

        for appt in appointments:
            patient = self.session.query(User).filter_by(uuid=appt.patient_id).first()
            self.appointments_tree.insert("", "end", values=(appt.id, appt.scheduled_time.strftime("%Y-%m-%d %H:%M"), appt.reason, patient.full_name, appt.status.value))

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
        self.LoadTable()
        self.reason_entry.delete(0, tk.END)
        self.datetime_entry.delete(0, tk.END)

    def EditAppointment(self):
        if self.appointments_tree:
            selection = self.appointments_tree.selection()
            if not selection:
                showinfo("Alert", "There is nothing selected.")
                return
            
            selectedItem = self.appointments_tree.item(selection[0])["values"]
            appt = self.session.query(models.Appointment).where(models.Appointment.id == selectedItem[0]).one_or_none()
            switch_to_window('create_appointment', onCreateArgs=(self.current_user, appt))
        

    def CancelAppointment(self):
        if self.appointments_tree:
            selection = self.appointments_tree.selection()
            
            if not selection:
                return
            
            try:
                selectedItem = self.appointments_tree.item(selection[0])["values"]
                
                appt = self.session.query(models.Appointment).where(models.Appointment.id == selectedItem[0]).one_or_none()
                
                if appt:
                    self.session.delete(appt)
                    self.session.commit()
                    
                showinfo("Alert", "Successfully cancelled appointment.")
                self.LoadTable()
            except Exception as e:
                print(f"Error: {e}")
                showinfo("Alert", "Failed to delete appointment.")

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

