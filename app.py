import frames.forget_password
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import frames
import frames.landing
import frames.login
import frames.patient_profile
import frames.register
import frames.main_menu
import fractions
import models
import tkinter as tk
from tkinter import ttk
from window_manager import add_window, switch_to_window
from database import DatabaseManager
import enum

engine = create_engine("sqlite:///hospital.db", echo=False)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session: Session = Session()
dbManager = DatabaseManager(session)
    
def main():
    # Register Windows
    add_window("login", frames.login.Login, (session, None, lambda: switch_to_window('main')))
    add_window("forget_password", frames.forget_password.ForgetPassword)
    # add_window("reset_password", frames.reset_password.ResetPassword)
    add_window("register", frames.register.Register, (session,))
    add_window("main", frames.main_menu.MainMenu)
    add_window("landing", frames.landing.LandingFrame)
    # add_window("patient_profile", frames.patient_profile.PatientProfile)

    # Open first window
    switch_to_window('landing')


if __name__ == "__main__":
    main()