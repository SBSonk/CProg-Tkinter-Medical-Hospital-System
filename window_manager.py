import tkinter as tk

windows = {}

# use this to add a window that can be switched to
def add_window(window_name, frame: tk.Frame):
    frame.grid(row=0, column=0)
    windows[window_name] = frame

# switches to window
def switch_to_window(window_name):
    for key, value in windows.items():
        if window_name is key:
            value.tkraise()
