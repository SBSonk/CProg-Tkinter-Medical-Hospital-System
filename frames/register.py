import tkinter as tk
import models
from sqlalchemy.orm import Session
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

entry_font = ("Arial", 12)
    
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
        
        back_button = ttk.Button(frame, text="Back", command=self.go_back)
        back_button.grid(row=0, column=0, pady=10, sticky='nw')

        ttk.Label(frame, text="Create New User", font=("Arial", 24, 'bold')).grid(
            row=0, column=1, pady=10
        )

        # USER COLUMN
        ttk.Label(frame, text="User Details", font=entry_font).grid(
            row=1, column=0, pady=10
        )

        roles = [e.value for e in models.UserRole]
        self.cmb_role = ttk.Combobox(frame, values=roles, width=18, state='readonly', font=entry_font, )
        self.cmb_role.set(roles[0])
        self.cmb_role.bind('<<ComboboxSelected>>', self.on_role_select)
        self.cmb_role.grid(row=2, column=0, ipady=7.5, ipadx=30)

        self.ent_username = PlaceholderEntry(
            frame,
            is_password=False,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Username",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_username.grid(row=3, column=0, ipady=7.5, ipadx=30)

        self.ent_password = PlaceholderEntry(
            frame,
            is_password=True,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Password",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_password.grid(row=4, column=0, ipady=7.5, ipadx=30)

        # ACCOUNT COLUMN
        ttk.Label(frame, text="Account Details", font=entry_font).grid(
            row=1, column=1, pady=10
        )

        self.ent_name = PlaceholderEntry(
            frame,
            is_password=False,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Name",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_name.grid(row=2, column=1, ipady=7.5, ipadx=30)

        gender_frame = tk.Frame(frame)
        gender_frame.grid(row=3, column=1, pady=10)

        self.gender_var = tk.StringVar()
        self.gender_var.set('male')  # Default value

        # Radio buttons in a 1x4 grid
        self.rb_male = ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="male")
        self.rb_female = ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="female")
        self.rb_nonbinary = ttk.Radiobutton(gender_frame, text="Non-binary", variable=self.gender_var, value="non-binary")
        self.rb_other = ttk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value="other")

        # Grid the radio buttons in the gender_frame
        self.rb_male.grid(row=0, column=0, sticky="w")
        self.rb_female.grid(row=0, column=1, sticky="w")
        self.rb_nonbinary.grid(row=0, column=2, sticky="w")
        self.rb_other.grid(row=0, column=3, sticky="w")

        self.ent_age = ttk.Spinbox(frame, from_=0, to=100, width=18, font=entry_font)
        self.ent_age.set(18)
        self.ent_age.grid(row=4, column=1, ipady=7.5, ipadx=33)

        self.ent_contact = PlaceholderEntry(
            frame,
            is_password=True,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Contact No.",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_contact.grid(row=5, column=1, ipady=7.5, ipadx=30)

        # PATIENT COLUMN
        ttk.Label(frame, text="Patient Details", font=entry_font).grid(
            row=1, column=2, pady=10
        )

        patient_form_elements = []
        self.ent_diseases = PlaceholderEntry(
            frame,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Chronic Diseases",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_diseases.grid(row=2, column=2, ipady=7.5, ipadx=30)
        
        patient_form_elements.append(self.ent_diseases)

        self.ent_allergies = PlaceholderEntry(
            frame,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Allergies",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_allergies.grid(row=3, column=2, ipady=7.5, ipadx=30)
        
        patient_form_elements.append(self.ent_allergies)

        self.ent_treatments = PlaceholderEntry(
            frame,
            normal_font=entry_font,
            placeholder_font=entry_font,
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

    def go_back(self):
        switch_to_window('landing')
