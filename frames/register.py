import tkinter as tk
import models
from tkinter import messagebox
from sqlalchemy.orm import Session
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window

entry_font = ("Arial", 12)
    
class Register(tk.Frame):
    def disable_patient_form(self):
        for ent in self.patient_form_elements:
                if isinstance(ent, PlaceholderEntry):       
                    ent.set_disabled(True)
    
    def enable_patient_form(self):
        for ent in self.patient_form_elements:
                if isinstance(ent, PlaceholderEntry):       
                    ent.set_disabled(False)      
    
    def on_role_select(self, event):
        selected_role = self.cmb_role.get()
        
        if selected_role == 'PATIENT':
            self.enable_patient_form()
        else:
            self.disable_patient_form()

    def register_account(self):
        if self.user_to_edit:
            # Update logic
            u = self.user_to_edit
            u.role = models.UserRole(self.cmb_role.get())
            u.full_name = self.ent_name.get_text().strip()
            u.age = int(self.ent_age.get())
            u.gender = self.gender_var.get()
            u.contact_info = self.ent_contact.get_text().strip()

            if u.role == models.UserRole.PATIENT:
                patient = self.session.query(models.Patient).filter_by(user_id=u.uuid).first()
                if not patient:
                    patient = models.Patient(user_id=u.uuid)
                    self.session.add(patient)
                patient.diseases = self.ent_diseases.get().strip()
                patient.allergies = self.ent_allergies.get().strip()
                patient.treatments = self.ent_treatments.get().strip()

            self.session.commit()
            showinfo("Alert", "User updated successfully!")
        else:
            self.register_account()  # Original logic
            showinfo("Alert", "User created successfully!")

        switch_to_window("user_account_module", onCreateArgs=(self.current_user,))
        
    def __init__(self, master, session: Session, current_user, user_to_edit: models.User = None):
        super().__init__(master)
        self.session = session
        self.current_user = current_user
        self.user_to_edit = user_to_edit

        frame = tk.Frame(self)

        frame.grid_rowconfigure(3, pad=10)
        frame.grid_rowconfigure(5, pad=10)
        
        back_button = ttk.Button(frame, text="Back", command=self.go_back)
        back_button.grid(row=1, column=0, pady=10, sticky='nw')

        if user_to_edit:
            ttk.Label(frame, text="Edit User", font=("Arial", 24, 'bold')).grid(
            row=0, column=1, pady=10
            )
        else:
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

        self.ent_security_question = PlaceholderEntry(
            frame,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Security Question",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_security_question.grid(row=5, column=0, ipady=7.5, ipadx=30)

        self.ent_security_answer = PlaceholderEntry(
            frame,
            normal_font=entry_font,
            placeholder_font=entry_font,
            placeholder_text="Security Answer",
            placeholder_color="#bfbfbf",
            text_color="black",
        )
        self.ent_security_answer.grid(row=6, column=0, ipady=7.5, ipadx=30)


        # ACCOUNT COLUMN
        ttk.Label(frame, text="Account Details", font=entry_font).grid(
            row=1, column=1, pady=10
        )

        self.ent_name = PlaceholderEntry(
            frame,
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
        self.disable_patient_form()

        save_text = "Create Account" if not user_to_edit else "Save Changes"
        self.btn_register = ttk.Button(
            frame,
            text=save_text,
            padding=(330, 12.5),
            command=self.register_account,
        )
        self.btn_register.grid(row=7, columnspan=3, pady=(50,10))

        frame.pack(padx=15, pady=15)
        
        if self.user_to_edit:
            self.populate_fields()

    def populate_fields(self):
        self.ent_security_question.set_disabled(True)
        self.ent_security_answer.set_disabled(True)
        self.ent_password.set_disabled(True)
        
        u = self.user_to_edit
        self.ent_username.set_text(u.username)
        self.ent_username.config(state='disabled')  # can't change username
        self.cmb_role.set(u.role.value)
        self.ent_name.set_text(u.full_name)
        self.ent_age.set(u.age)
        self.gender_var.set(u.gender)
        self.ent_contact.set_text(u.contact_info)

        if u.role == models.UserRole.PATIENT:
            patient = self.session.query(models.Patient).filter_by(user_id=u.uuid).first()
            if patient:
                self.ent_diseases.set_text(patient.diseases)
                self.ent_allergies.set_text(patient.allergies)
                self.ent_treatments.set_text(patient.treatments)
            self.enable_patient_form()

    def go_back(self):
        switch_to_window("user_account_module", onCreateArgs=(self.current_user,))
