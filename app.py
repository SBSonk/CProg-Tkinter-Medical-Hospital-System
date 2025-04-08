import frames.forget_password
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

engine = create_engine("sqlite:///hospital.db", echo=True)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
    
def main():
    # todo: rerun at home
    # login_window = frames.login.Login(root, session, lambda: switch_to_window("main"))
    # register_window = frames.register.Register(root, session)
    # main_window = frames.main_menu.MainMenu(root)

    add_window("login", frames.login.Login, (session, None, lambda: switch_to_window('main')))
    # add_window("register", register_window)
    add_window("main", frames.main_menu.MainMenu)

    switch_to_window('login')


if __name__ == "__main__":
    main()

