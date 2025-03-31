import tkinter as tk

class Login(tk.Frame):
    ent_username: tk.Entry = None
    ent_password: tk.Entry = None

    def __init__(self, master):
        super().__init__(master)

        fr_text = tk.Frame(master, bg='gray')
        tk.Label(fr_text, text='LOGIN').pack()

        fr_text.grid(row=0, column=0)

        self.ent_username = tk.Entry(fr_text)
        self.ent_username.pack()
        self.ent_password = tk.Entry(fr_text)
        self.ent_password.pack()
        

    