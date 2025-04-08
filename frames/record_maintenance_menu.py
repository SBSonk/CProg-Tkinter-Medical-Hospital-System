import tkinter as tk
from tkinter import ttk
from window_manager import switch_to_window

class RecordMaintenanceMenu(tk.Frame):
    def __init__(self, master, session, current_user):
        super().__init__(master)
        self.session = session
        self.current_user = current_user

        ttk.Label(self, text="Record Maintenance", font=('Arial', 16)).pack(pady=10)

        ttk.Button(self, text="User Accounts", width=30,
                   command=lambda: switch_to_window("user_account_module", onCreateArgs=(session, current_user))).pack(pady=5)

        ttk.Button(self, text="Patient Information List", width=30,
                   command=lambda: switch_to_window("patient_info_module", onCreateArgs=(session, current_user))).pack(pady=5)

        ttk.Button(self, text="Back to Main Menu", width=30,
                   command=lambda: switch_to_window("main_menu", onCreateArgs=(session, current_user))).pack(pady=20)
