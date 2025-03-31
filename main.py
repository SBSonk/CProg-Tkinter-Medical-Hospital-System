from flask import Flask
from models import db, bcrypt
import tkinter as tk
from frames.login import Login

app = Flask(__name__)
app.config.from_pyfile('config.py')

bcrypt.init_app(app)
db.init_app(app)

# todo: need to create database
root = tk.Tk()

# todo: rerun at home
login_window = Login(root)
login_window.pack()

if __name__ == '__main__':
    app.run()
    root.mainloop()