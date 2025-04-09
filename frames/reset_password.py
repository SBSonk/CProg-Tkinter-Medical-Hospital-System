import tkinter as tk
import models
from sqlalchemy.orm import Session
from sqlalchemy import Select
from tkinter import ttk
from tkinter.messagebox import showinfo
from custom_widgets import PlaceholderEntry, HyperlinkLabel
from window_manager import switch_to_window
from tkinter.messagebox import showinfo

class ResetPassword(tk.Frame):
    session: Session = None

    user_to_edit: models.User = None

    def submitPassword(self):
        password = self.ent_password.get()
        confirm_password = self.ent_password_confirm.get()
        security_answer = self.ent_security_question.get()
        
        if security_answer == "":
            showinfo("Alert", "Enter security answer.")
            return
        
        if not self.user_to_edit.check_security_answer(security_answer):
            showinfo("Alert", "Wrong security answer.")
            return
        
        if password == "" or confirm_password == "":
            showinfo("Alert", "Please enter a password twice.")
            return
            
        if password != confirm_password:
            showinfo("Alert", "Passwords are not the same.")
            return
        
        try:
            self.user_to_edit.set_password(password)
            self.session.commit()
            showinfo("Alert", "Password updated successfully.")
            switch_to_window('login')
        except Exception as e:
            self.session.rollback()
            showinfo("Error", "User failed to update.")
            print(f"Database error: {e}")

    def __init__(self, master, session, user_to_edit: models.User):
        super().__init__(master)
        self.user_to_edit = user_to_edit
        self.session = session

        frame = tk.Frame(self, width=384, height=540)
        frame.grid_rowconfigure(0, pad=0)
        frame.grid_rowconfigure(2, pad=20)
        frame.grid_rowconfigure(3, pad=20)
        ttk.Label(frame, text=f'Reset password', font=('Arial', 24), justify=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=10)
        
        
        # Security Answer
        security_frame = tk.Frame(frame, pady=10)
        ttk.Label(security_frame, text=user_to_edit.security_question, font=('Arial', 16)).pack(pady=5)
        
        self.ent_security_question = PlaceholderEntry(security_frame, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Enter Answer', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_security_question.pack(ipady=7.5)
        security_frame.grid(row=1, column=0)
        
        # Password Entry
        self.ent_password = PlaceholderEntry(frame, 
                                             is_password=True, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Enter Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password.grid(row=2, column=0, ipady=7.5)

        self.ent_password_confirm = PlaceholderEntry(frame, 
                                             is_password=True, 
                                             normal_font=('Arial', 16), 
                                             placeholder_font=('Arial', 16), 
                                             placeholder_text='Confirm Password', 
                                             placeholder_color='#bfbfbf', 
                                             text_color='black')
        self.ent_password_confirm.grid(row=3, column=0, ipady=7.5)

        self.btn_next = ttk.Button(frame, text='Reset Password', padding=(50, 12.5), command=self.submitPassword)
        self.btn_next.grid(row=4, columnspan=2, pady=10, sticky='ew')

        frame.pack(padx=15, pady=15)    