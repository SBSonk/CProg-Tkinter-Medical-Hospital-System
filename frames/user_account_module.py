import tkinter as tk
from tkinter import ttk, messagebox
from models import User
from window_manager import switch_to_window
from tkinter.messagebox import showinfo

class UserAccountModule(tk.Frame):
    def __init__(self, master, session, current_user):
        super().__init__(master)
        self.session = session
        self.current_user = current_user
        self.selected_user = None

        ttk.Label(self, text="User Account Management", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Role", "Name"), show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, columnspan=2, padx=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # ttk.Button(self, text="Register User", command=lambda: switch_to_window("register", onCreateArgs=(current_user,))).grid(row=2, column=0, pady=5)
        # ttk.Button(self, text="Edit User", command=self.edit_user).grid(row=2, column=0, columnspan=2, pady=10)
        # ttk.Button(self, text="Delete User", command=self.delete_user).grid(row=2, column=1, pady=5)
        # ttk.Button(self, text="Back", command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).grid(row=3, column=0, columnspan=2, pady=10)

        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(frame)
        button_frame.pack()
        buttons = [
            ttk.Button(button_frame, text="Register User", command=self.register_user),
            ttk.Button(button_frame, text="Edit User", command=self.EditUser),
            ttk.Button(button_frame, text="Delete User", command=self.delete_user)
        ]

        i = 0
        for b in buttons:
            b.grid(row=0, column=i)
            i += 1
                
        ttk.Button(frame, text="Back to Main Menu", width=30,
                   command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).pack(pady=20)

        self.load_users()

    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        users = self.session.query(User).all()
        for user in users:
            self.tree.insert("", "end", values=(user.uuid, user.username, user.role.value, user.full_name))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_user = item["values"]

    def EditUser(self):
        if self.tree:
            selection = self.tree.selection()
            if not selection:
                showinfo("Alert", "There is nothing selected.")
                return
            
            selectedItem = self.tree.item(selection[0])["values"]
            user = self.session.query(User).where(User.uuid == selectedItem[0]).one_or_none()
            
            switch_to_window('register', onCreateArgs=(self.current_user, user))
        
    def delete_user(self):
        if not self.selected_user:
            messagebox.showwarning("Select User", "Please select a user to delete.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        if confirm:
            user = self.session.query(User).filter_by(uuid=self.selected_user[0]).first()
            self.session.delete(user)
            self.session.commit()
            self.load_users()

    def register_user(self):
        switch_to_window("register", onCreateArgs=(self.current_user,))
