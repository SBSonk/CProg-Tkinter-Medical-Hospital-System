import os
import frames.create_appointment
import frames.create_doctor_note
import frames.doctors_notes
import frames.forget_password
import frames.reset_password
import frames.login
import frames.landing
import frames.register
import frames.main_menu
import frames.appointments
import frames.appointment_patient
import frames.record_maintenance_menu
import frames.user_account_module
import frames.patient_info_module

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models
import tkinter as tk
from window_manager import add_window, switch_to_window
from database import DatabaseManager

DB_PATH = "hospital.db"

# Check if DB file already exists
is_new_database = not os.path.exists(DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
dbManager: DatabaseManager = DatabaseManager(session)

current_user = {"user": None}  # Holds the logged-in user

def seed_initial_data():    
    if not session.query(models.User).first():
        admin = models.User(
            username="admin",
            password="admin123",
            full_name="Nurse Joy",
            security_question="First pet's name?",
            security_answer="Meowth",
            role=models.UserRole.ADMIN,
            age=30,
            gender="female",
            contact_info="123-456-7890"
        )
        session.add(admin)
        session.commit()

def main():
    if is_new_database:
        seed_initial_data()

    add_window("login", frames.login.Login, (session, current_user))
    add_window("forget_password", frames.forget_password.ForgetPassword, (dbManager,))
    add_window("reset_password", frames.reset_password.ResetPassword, (session,))
    
    add_window("register", frames.register.Register, (session,))
    add_window("create_appointment", frames.create_appointment.CreateAppointment, (session, dbManager))
    add_window("create_doctor_note", frames.create_doctor_note.CreateDoctorNote, (session, dbManager))
    
    add_window("main_menu", frames.main_menu.MainMenu, (session, ))
    add_window("appointments", frames.appointments.Appointments, (dbManager, session))
    add_window("doctors_notes", frames.doctors_notes.DoctorsNotes, (dbManager, session))
    add_window("landing", frames.landing.LandingFrame)
    add_window("record_maintenance_menu", frames.record_maintenance_menu.RecordMaintenanceMenu, (session, ))
    add_window("user_account_module", frames.user_account_module.UserAccountModule, (session, ))
    add_window("patient_info_module", frames.patient_info_module.PatientInfoModule, (session, ))

    # create as nurse joy
    switch_to_window("landing")

if __name__ == "__main__":
    main()
