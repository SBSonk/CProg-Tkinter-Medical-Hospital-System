import frames.forget_password
import frames.reset_password
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import frames
import frames.login
import frames.register
import frames.main_menu
import fractions
import models
import tkinter as tk
from tkinter import ttk
from window_manager import add_window, switch_to_window
import enum
from database import DatabaseManager

engine = create_engine("sqlite:///hospital.db", echo=False)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session: Session = Session()
dbManager: DatabaseManager = DatabaseManager(session)
    
def main():
    # Register Windows
    add_window("login", frames.login.Login, (session, None, lambda: switch_to_window('main')))
    add_window("forget_password", frames.forget_password.ForgetPassword, (dbManager,))
    add_window("reset_password", frames.reset_password.ResetPassword)
    add_window("main", frames.main_menu.MainMenu)

    # test user
    # dbManager.create_user("adam", "tite", models.UserRole.ADMIN, "georg") # id = 1

    # Open first window 
    switch_to_window('login')

    

if __name__ == "__main__":
    main()

