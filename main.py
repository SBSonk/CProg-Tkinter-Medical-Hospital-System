from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from frames.login import Login
from frames.register import Register
import models 
import tkinter as tk
from tkinter import ttk
from window_manager import add_window, switch_to_window

engine = create_engine('sqlite:///hospital.db', echo=True)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

root = tk.Tk()
# root.geometry('640x480') # full window size
root.geometry('350x432') # login size
root.pack_propagate(0)
root.resizable(0, 0)

def main():
    # todo: rerun at home
    login_window = Login(root, session, lambda: switch_to_window('main'))
    register_window = Register(root, session)
    main_window = tk.Frame(root, width=350, height=432)
    tk.Label(main_window, text='hello user i dont know').pack()

    add_window('login', login_window)
    add_window('register', register_window)
    add_window('main', main_window)

    switch_to_window('register')
        
if __name__ == '__main__':
    main()
    root.mainloop()