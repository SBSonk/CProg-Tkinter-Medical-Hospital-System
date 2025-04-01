from models import db, bcrypt
import tkinter as tk
from frames.login import Login

# bcrypt.init_app(app)
# db.init_app(app)

# todo: need to create database
root = tk.Tk()

# todo: rerun at home
login_window = Login(root)

if __name__ == '__main__':
    root.mainloop()