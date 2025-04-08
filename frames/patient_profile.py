import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from database import engine
from models import User, MedicalHistory

Session = sessionmaker(bind=engine)

class PatientProfile:
    def __init__(self, master, user_id):
        self.master = master
        self.master.title("Patient Profile")
        self.session = Session()
        self.user_id = user_id

        self.load_profile()

    def load_profile(self):
        user = self.session.query(User).filter_by(id=self.user_id).first()
        medical_history = self.session.query(MedicalHistory).filter_by(user_id=self.user_id).first()

        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        # Personal Info
        tk.Label(self.master, text="Patient Profile", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Full Name:", "Username:", "Age:", "Gender:", "Contact:"]
        values = [user.fullname, user.username, user.age, user.gender, user.contact]

        for i, (label, value) in enumerate(zip(labels, values), start=1):
            tk.Label(self.master, text=label).grid(row=i, column=0, sticky="w", padx=10)
            tk.Label(self.master, text=value).grid(row=i, column=1, sticky="w")

        # Medical History
        if medical_history:
            tk.Label(self.master, text="Chronic Diseases:").grid(row=6, column=0, sticky="w", padx=10, pady=(10, 0))
            tk.Label(self.master, text=medical_history.chronic_diseases).grid(row=6, column=1, sticky="w", pady=(10, 0))

            tk.Label(self.master, text="Allergies:").grid(row=7, column=0, sticky="w", padx=10)
            tk.Label(self.master, text=medical_history.allergies).grid(row=7, column=1, sticky="w")

        else:
            tk.Label(self.master, text="No medical history found.").grid(row=6, column=0, columnspan=2, pady=10)

        # Button to Edit Profile (next step)
        tk.Button(self.master, text="Edit Profile", command=self.edit_profile).grid(row=8, column=0, columnspan=2, pady=20)

    def edit_profile(self):
        # Placeholder function – will implement next
        messagebox.showinfo("Edit", "This will open the edit profile window.")

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = PatientProfile(root, user_id=1)  # Replace with actual user ID from login
    root.mainloop()
