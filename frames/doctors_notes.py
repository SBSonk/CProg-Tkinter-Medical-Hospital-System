import tkinter as tk
import models
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from models import Appointment, User, UserRole
from datetime import datetime
from window_manager import switch_to_window
from database import DatabaseManager
from tkinter.messagebox import showinfo

class DoctorsNotes(tk.Frame):
    selectedNote = None
    
    def OnItemSelect(self, event):
        selected_item = event.widget.selection()
        if selected_item:
            item_id = selected_item[0]
            values = event.widget.item(item_id, "values")
            self.selectedNote = values
                
    def __init__(self, master, dbManager: DatabaseManager, session: Session, current_user: User):
        super().__init__(master)
        self.session = session
        self.current_user = current_user
        self.dbManager = dbManager

        frame = ttk.Frame(self)
        frame.pack(padx=15, pady=15)
        
        ttk.Label(frame, text="Doctor's Notes", font=("Arial", 24, 'bold')).pack(pady=10)
        
        # Proper column identifiers and widths
        columns = [
            ("ID", 25),
            ("PATIENT NAME", 100),
            ("NOTE", 400),
            ("CREATED BY", 100)
        ]

        # Extract just the column names for the Treeview
        col_ids = [col[0] for col in columns]

        tree = ttk.Treeview(frame, columns=col_ids, show="headings", selectmode="browse")

        # Configure each column's heading and width
        for name, width in columns:
            tree.heading(name, text=name)
            tree.column(name, width=width)

        tree.pack(fill="both", expand=True)
        
        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.pack()
        buttons = [
            ttk.Button(button_frame, text="Add Note", command=self.CreateNote),
            ttk.Button(button_frame, text="Edit Note", command=self.EditNote),
            ttk.Button(button_frame, text="Delete Note", command=self.DeleteNote)
        ]

        ttk.Button(self, text="Back to Main Menu", width=30,
                   command=lambda: switch_to_window("main_menu", onCreateArgs=(current_user,))).pack(pady=20)
        
        i = 0
        for b in buttons:
            b.grid(row=0, column=i)
            i += 1
            
        self.tree = tree
        self.LoadTable()
        
        
        
        tree.bind("<<TreeViewSelect>>", self.OnItemSelect)
            
    def LoadTable(self):
        tree = self.tree
        data = self.dbManager.get_all_doctor_notes()

        # Clear existing items first
        for item in tree.get_children():
            tree.delete(item)

        for note in data:
            patient_user = self.dbManager.get_user(note.patient_id)
            doctor_user = self.dbManager.get_user(note.created_by_id)
            row = (
                note.id,
                patient_user.full_name if patient_user else "Unknown",
                note.note,
                doctor_user.full_name if doctor_user else "Unknown"
            )
            tree.insert("", tk.END, values=row)
                
    def CreateNote(self):
        switch_to_window('create_doctor_note', onCreateArgs=(self.current_user,))
        
    def EditNote(self):
        if self.tree:
            selection = self.tree.selection()
            if not selection:
                return
            
            selectedItem = self.tree.item(selection[0])["values"]
            note = self.session.query(models.DoctorNote).where(models.DoctorNote.id == selectedItem[0]).one_or_none()
            
            switch_to_window('create_doctor_note', onCreateArgs=(self.current_user, note))
        
    def DeleteNote(self):
        if self.tree:
            selection = self.tree.selection()
            if not selection:
                return
            
            try:
                selectedItem = self.tree.item(selection[0])["values"]
                
                note = self.session.query(models.DoctorNote).where(models.DoctorNote.id == selectedItem[0]).one_or_none()
                
                if note:
                    self.session.delete(note)
                    self.session.commit()
                    
                showinfo("Alert", "Successfully deleted note.")
                self.LoadTable()
            except Exception as e:
                print(f"Error: {e}")
                showinfo("Alert", "Failed to delete note.")



