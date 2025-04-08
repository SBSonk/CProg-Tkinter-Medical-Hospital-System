import tkinter as ttk
from models import User, MedicalHistory

class PatientProfile:
    def __init__(self, master):
        super().__init__(master)


        # Title
        title_label = ttk.Label(self, text="Name: ", font=("Arial", 16))
        title_label.pack(pady=20)
        title_label = ttk.Label(self, text="Age: ", font=("Arial", 16))
        title_label.pack(pady=20)
        title_label = ttk.Label(self, text="Gender: ", font=("Arial", 16))
        title_label.pack(pady=20)
        title_label = ttk.Label(self, text="Contact Information: ", font=("Arial", 16))
        title_label.pack(pady=20)