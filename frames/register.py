import tkinter as tk
import models
from sqlalchemy.orm import Session
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

class Register(tk.Frame):
    def disablePatientForm(self):
        for ent in self.patient_form_elements:
                if isinstance(ent, PlaceholderEntry):       
                    ent.set_disabled(True)
    
    def enablePatientForm(self):
        for ent in self.patient_form_elements:
                if isinstance(ent, PlaceholderEntry):       
                    ent.set_disabled(False)      
    
    def on_role_select(self, event):
        selected_role = self.cmb_role.get()
        
        if selected_role == 'patient':
            self.enablePatientForm()
        else:
            self.disablePatientForm()
        
        match selected_role:
            case 'admin':
                pass
            
            case 'doctor':
                pass
            
            case 'nurse':
                pass
            
            case 'patient':
                pass

    def register_account(self):
        # todo: validate contents

        new_user = models.User(
            username=self.ent_username.get_text(), password=self.ent_password.get_text()
        )

        print(new_user)

        try:
            self.session.add(new_user)
            self.session.commit()
            print("User creation success.")
            showinfo("Alert", "User successfully created!")
        except Exception as e:
            print("User creation failed.")
            print(e)
            showinfo("Alert", "User successfully failed!")

    def __init__(self, master, session: Session):
        super().__init__(master)
        self.session = session

        frame = tk.Frame(self)

        frame.grid_rowconfigure(3, pad=10)
        frame.grid_rowconfigure(5, pad=10)
        
        ttk.Button(frame, text="Back").grid(
            row=0, column=0, pady=10, sticky='nw'
        )

        ttk.Label(frame, text="Create New User", font=("Arial", 24, 'bold')).grid(
            row=0, column=1, pady=10
        )

        # USER COLUMN
        ttk.Label(frame, text="User Details", font=("Arial", 12)).grid(
            row=1, column=0, pady=10
        )

        roles = [e.value for e in models.UserRole]
        self.cmb_role = ttk.Combobox(frame, values=roles, width=18, state='readonly', font=("Arial", 12), )
        self.cmb_role.set(roles[0])
        self.cmb_role.bind('<<ComboboxSelected>>', self.on_role_select)
        self.cmb_role.grid(row=2, column=0, ipady=7.5, ipadx=30)

        self.ent_username = PlaceholderEntry(
            frame,
            is_password=False,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Username",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_username.grid(row=3, column=0, ipady=7.5, ipadx=30)

        self.ent_password = PlaceholderEntry(
            frame,
            is_password=True,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Password",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_password.grid(row=4, column=0, ipady=7.5, ipadx=30)

        # ACCOUNT COLUMN
        ttk.Label(frame, text="Account Details", font=("Arial", 12)).grid(
            row=1, column=1, pady=10
        )

        self.ent_name = PlaceholderEntry(
            frame,
            is_password=False,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Name",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_name.grid(row=2, column=1, ipady=7.5, ipadx=30)

        self.ent_gender = PlaceholderEntry(
            frame,
            is_password=False,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Gender",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_gender.grid(row=3, column=1, ipady=7.5, ipadx=30)

        self.ent_age = PlaceholderEntry(
            frame,
            is_password=True,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Age",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_age.grid(row=4, column=1, ipady=7.5, ipadx=30)

        self.ent_contact = PlaceholderEntry(
            frame,
            is_password=True,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Contact No.",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_contact.grid(row=5, column=1, ipady=7.5, ipadx=30)

        # PATIENT COLUMN
        ttk.Label(frame, text="Patient Details", font=("Arial", 12)).grid(
            row=1, column=2, pady=10
        )

        patient_form_elements = []
        self.ent_diseases = PlaceholderEntry(
            frame,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Chronic Diseases",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_diseases.grid(row=2, column=2, ipady=7.5, ipadx=30)
        
        patient_form_elements.append(self.ent_diseases)

        self.ent_allergies = PlaceholderEntry(
            frame,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Allergies",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_allergies.grid(row=3, column=2, ipady=7.5, ipadx=30)
        
        patient_form_elements.append(self.ent_allergies)

        self.ent_treatments = PlaceholderEntry(
            frame,
            normal_font=("Arial", 12),
            placeholder_font=("Arial", 12),
            placeholder_text="Past Treatments",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_treatments.grid(row=4, column=2, ipady=7.5, ipadx=30)
        
        patient_form_elements.append(self.ent_treatments)
        self.patient_form_elements = patient_form_elements
        self.disablePatientForm()

        self.btn_register = ttk.Button(
            frame,
            text="Create Account",
            padding=(330, 12.5),
            command=self.register_account,
        )
        self.btn_register.grid(row=6, columnspan=3, pady=(50,10))

        frame.pack(padx=10, pady=10)
