import tkinter as tk
from tkinter import ttk
from models import User, UserRole
from window_manager import switch_to_window

class PatientInfoModule(tk.Frame):
    def __init__(self, master, session, current_user):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        ttk.Label(self, text="Patient Information", font=('Arial', 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Name", "Age", "Gender", "Contact"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        ttk.Button(self, text="Back", command=lambda: switch_to_window("record_maintenance_menu", onCreateArgs=(session, current_user))).pack(pady=10)

        self.load_patients()

    def load_patients(self):
        self.tree.delete(*self.tree.get_children())
        patients = self.session.query(User).filter_by(role=UserRole.PATIENT).all()
        for patient in patients:
            self.tree.insert("", "end", values=(patient.uuid, patient.username, patient.full_name, patient.age, patient.gender, patient.contact_info))
