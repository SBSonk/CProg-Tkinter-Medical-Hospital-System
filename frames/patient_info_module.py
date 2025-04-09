import tkinter as tk
from tkinter import ttk
from models import User, UserRole
from window_manager import switch_to_window

class PatientInfoModule(tk.Frame):
    def __init__(self, master, session, current_user):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        frame = ttk.Frame(self)
        frame.pack(padx=15, pady=15)
        
        # Title Label
        ttk.Label(frame, text="Patient Information", font=("Arial", 24, 'bold')).pack(pady=10)
        
        # Proper column identifiers and widths for the table
        columns = [
            ("ID", 25),
            ("USERNAME", 100),
            ("NAME", 150),
            ("AGE", 50),
            ("GENDER", 80),
            ("CONTACT", 150)
        ]
        
        # Extract just the column names for the Treeview
        col_ids = [col[0] for col in columns]

        # Treeview setup
        tree = ttk.Treeview(frame, columns=col_ids, show="headings", selectmode="browse")

        # Configure each column's heading and width
        for name, width in columns:
            tree.heading(name, text=name)
            tree.column(name, width=width)

        tree.pack(fill="both", expand=True)
        
        # Buttons frame
        # button_frame = tk.Frame(frame)
        # button_frame.pack(pady=10)
        
        # Back Button
        ttk.Button(self, text="Back", width=30, command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).pack(pady=20)

        self.tree = tree
        self.load_patients()

    def load_patients(self):
        # Fetching patient data from the database
        self.tree.delete(*self.tree.get_children())
        patients = self.session.query(User).filter_by(role=UserRole.PATIENT).all()
        
        # Insert rows into the treeview
        for patient in patients:
            row = (
                patient.uuid, 
                patient.username, 
                patient.full_name, 
                patient.age, 
                patient.gender, 
                patient.contact_info
            )
            self.tree.insert("", "end", values=row)
