import tkinter as tk
import models
from sqlalchemy.orm import Session

class Register(tk.Frame):
    ent_username: tk.Entry = None
    ent_password: tk.Entry = None
    btn_login: tk.Button = None

    session = None

    def register_account(self):
        # validate contents

        new_user = models.User(
            username = self.ent_username.get(),
            password = self.ent_password.get()
        )

        print(new_user)

        try:
            self.session.add(new_user)
            self.session.commit()
            print('User creation success.')
        except Exception as e:
            print('User creation failed.')
            print(e)

    def __init__(self, master, session: Session):
        super().__init__(master)
        self.session = session

        fr_text = tk.Frame(master, bg='gray', padx=60, pady=15)
        tk.Label(fr_text, text='Register', font=('Arial', 24)).pack(pady=(0, 20))

        fr_text.grid(row=0, column=0)

        tk.Label(fr_text, text='Username').pack(anchor='w')
        self.ent_username = tk.Entry(fr_text)
        self.ent_username.pack(pady=(0, 10))

        tk.Label(fr_text, text='Password').pack(anchor='w', pady=(10, 0))
        self.ent_password = tk.Entry(fr_text, show='*')
        self.ent_password.pack()

        self.btn_register = tk.Button(fr_text, text='Create Account', padx=50, pady=10, command=self.register_account)
        self.btn_register.pack(pady=(20, 0))