import tkinter as tk
import models
from sqlalchemy import select
from sqlalchemy.orm import Session

class Login(tk.Frame):
    ent_username: tk.Entry = None
    ent_password: tk.Entry = None
    btn_login: tk.Button = None

    session: Session = None

    def login(self) -> bool:
        statement = select(models.User).where(models.User.username == self.ent_username.get())
        user: models.User = self.session.execute(statement).scalar_one_or_none()
        
        if not user:
            print('User does not exist.')
            return False
        
        if user.check_password(self.ent_password.get()):
            print('Logged in successfully.')
            return True
        else:
            print('Incorrect password.')
            return False

    def __init__(self, master, session: Session):
        super().__init__(master)
        self.session = session

        fr_text = tk.Frame(master, bg='gray', padx=60, pady=15)
        tk.Label(fr_text, text='LOGIN', font=('Arial', 24)).pack(pady=(0, 20))

        fr_text.grid(row=0, column=0)

        tk.Label(fr_text, text='Username').pack(anchor='w')
        self.ent_username = tk.Entry(fr_text)
        self.ent_username.pack(pady=(0, 10))

        tk.Label(fr_text, text='Password').pack(anchor='w', pady=(10, 0))
        self.ent_password = tk.Entry(fr_text, show='*')
        self.ent_password.pack()

        self.btn_login = tk.Button(fr_text, text='Login', padx=50, pady=10, command=self.login)
        self.btn_login.pack(pady=(20, 0))
        

    