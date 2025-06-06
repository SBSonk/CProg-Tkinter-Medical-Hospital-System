import tkinter as ttk
from ttkwidgets import Table
from sqlalchemy.orm import Session
from models import User, MedicalHistory

class PatientProfile:
    root = tk.Tk()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    style = ttk.Style(root)
    style.theme_use('alt')
    sortable = tk.BooleanVar(root, False)
    drag_row = tk.BooleanVar(root, False)
    drag_col = tk.BooleanVar(root, False)

    columns = ["A", "B", "C", "D", "E", "F", "G"]
    table = Table(root, columns=columns, sortable=sortable.get(), drag_cols=drag_col.get(),
                drag_rows=drag_row.get(), height=6)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100, stretch=False)

    # sort column A content as int instead of strings
    table.column('A', type=int)

    for i in range(12):
        table.insert('', 'end', iid=i,
                    values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))

    # add scrollbars
    sx = tk.Scrollbar(root, orient='horizontal', command=table.xview)
    sy = tk.Scrollbar(root, orient='vertical', command=table.yview)
    table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

    table.grid(sticky='ewns')
    sx.grid(row=1, column=0, sticky='ew')
    sy.grid(row=0, column=1, sticky='ns')
    root.update_idletasks()


    # toggle table properties
    def toggle_sort():
        table.config(sortable=sortable.get())


    def toggle_drag_col():
        table.config(drag_cols=drag_col.get())


    def toggle_drag_row():
        table.config(drag_rows=drag_row.get())


    frame = tk.Frame(root)
    tk.Checkbutton(frame, text='sortable', variable=sortable, command=toggle_sort).pack(side='left')
    tk.Checkbutton(frame, text='drag columns', variable=drag_col, command=toggle_drag_col).pack(side='left')
    tk.Checkbutton(frame, text='drag rows', variable=drag_row, command=toggle_drag_row).pack(side='left')
    frame.grid()
    root.geometry('400x200')

    root.mainloop()    
    def __init__(self, master):
        super().__init__(master)


        # Title
        title_label = ttk.Label(self, text="Name: ", font=("Arial", 16))
        title_label.pack(pady=20)
        title_label = ttk.Label(self, text="Age: ", font=("Arial", 16))
        title_label.pack(pady=20)
        title_label = ttk.Label(self, text="Gender: ", font=("Arial", 16))
        title_label.pack(pady=20)
        title_label = ttk.Label(self, text="Contact Information: ", font=("Arial", 16))
        title_label.pack(pady=20)

