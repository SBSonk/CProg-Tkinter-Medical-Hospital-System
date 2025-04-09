import frames.create_appointment
import frames.create_doctor_note
import frames.doctors_notes
import frames.forget_password
import frames.reset_password
import frames.login
import frames.landing
import frames.register
import frames.main_menu
import frames.appointment_nurse
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

engine = create_engine("sqlite:///hospital.db", echo=False)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
dbManager: DatabaseManager = DatabaseManager(session)

current_user = {"user": None}  # Holds the logged-in user

def main():
    add_window("login", frames.login.Login, (session, current_user))
    add_window("forget_password", frames.forget_password.ForgetPassword, (dbManager,))
    add_window("reset_password", frames.reset_password.ResetPassword, (session,))
    
    add_window("register", frames.register.Register, (session,))
    add_window("create_appointment", frames.create_appointment.CreateAppointment, (session, dbManager))
    add_window("create_doctor_note", frames.create_doctor_note.CreateDoctorNote, (session, dbManager))
    
    add_window("main_menu", frames.main_menu.MainMenu, (session, ))
    add_window("appointment_patient", frames.appointment_patient.AppointmentPatient)
    add_window("appointment_nurse", frames.appointment_nurse.AppointmentNurse)
    add_window("doctors_notes", frames.doctors_notes.DoctorsNotes, (dbManager, session))
    add_window("landing", frames.landing.LandingFrame)
    add_window("record_maintenance_menu", frames.record_maintenance_menu.RecordMaintenanceMenu)
    add_window("user_account_module", frames.user_account_module.UserAccountModule)
    add_window("patient_info_module", frames.patient_info_module.PatientInfoModule)

    # create as nurse joy
    # switch_to_window("create_doctor_note", onCreateArgs=(dbManager.get_user(1),))
    switch_to_window("landing")
    # switch_to_window("doctors_notes", onCreateArgs=(dbManager.get_user(3),))
    # switch_to_window("register")

if __name__ == "__main__":
    main()
