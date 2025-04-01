from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import frames.login
import frames.register
import models
import tkinter as tk
import frames
import sqlite3

# bcrypt.init_app(app)
engine = create_engine('sqlite:///hospital.db', echo=True)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# todo: need to create database
login = tk.Tk()
register = tk.Tk()

# todo: rerun at home
login_window = frames.login.Login(login, session)
register_window = frames.register.Register(register, session)

if __name__ == '__main__':
    login.mainloop()
    register.mainloop()