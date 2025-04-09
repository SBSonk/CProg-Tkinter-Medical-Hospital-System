import tkinter as tk
from tkinter import ttk, messagebox
from models import User
from window_manager import switch_to_window

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

        ttk.Button(self, text="Edit User", command=self.edit_user).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Delete User", command=self.delete_user).grid(row=2, column=1, pady=5)
        ttk.Button(self, text="Back", command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).grid(row=3, column=0, columnspan=2, pady=10)

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

    def edit_user(self):
        if not self.selected_user:
            messagebox.showwarning("Select User", "Please select a user to edit.")
            return

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit User")
        edit_window.geometry("300x300")

        user = self.session.query(User).filter_by(uuid=self.selected_user[0]).first()

        fields = {
            "Full Name": tk.StringVar(value=user.full_name),
            "Username": tk.StringVar(value=user.username),
            "Contact Info": tk.StringVar(value=user.contact_info),
        }

        row = 0
        for label, var in fields.items():
            ttk.Label(edit_window, text=label).grid(row=row, column=0, sticky="e", pady=5)
            ttk.Entry(edit_window, textvariable=var).grid(row=row, column=1, pady=5)
            row += 1

        def save_changes():
            user.full_name = fields["Full Name"].get()
            user.username = fields["Username"].get()
            user.contact_info = fields["Contact Info"].get()
            self.session.commit()
            self.load_users()
            edit_window.destroy()

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=row, column=0, columnspan=2, pady=10)

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

    def register(self):
        switch_to_window("register")
