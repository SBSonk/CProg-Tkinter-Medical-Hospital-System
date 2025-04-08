import frames.forget_password
import frames.reset_password
import frames.login
import frames.landing
import frames.register
import frames.main_menu
import frames.appointment_nurse
import frames.appointment_patient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models
import tkinter as tk
from window_manager import add_window, switch_to_window
from database import DatabaseManager

engine = create_engine("sqlite:///hospital.db", echo=False)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session: Session = Session()
dbManager: DatabaseManager = DatabaseManager(session)

current_user = {"user": None}  # Holds the logged-in user

def main():
    add_window("login", frames.login.Login, (session, current_user, lambda: switch_to_window("main")))
    add_window("forget_password", frames.forget_password.ForgetPassword, (dbManager,))
    add_window("reset_password", frames.reset_password.ResetPassword)
    add_window("register", frames.register.Register, (session,))
    add_window("main", frames.main_menu.MainMenu, (current_user,))
    add_window("appointment_patient", frames.appointment_patient.AppointmentPatient, (session, current_user))
    add_window("appointment_nurse", frames.appointment_nurse.AppointmentNurse, (session,))
    add_window("landing", frames.landing.LandingFrame)

    switch_to_window("landing")

if __name__ == "__main__":
    main()
