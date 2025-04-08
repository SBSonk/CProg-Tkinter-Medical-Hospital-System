import tkinter as tk

windows = {}

# use this to add a window that can be switched to
def add_window(window_name, frame: tk.Frame, variables: tuple = ()):
    windows[window_name] = frame
    windows[window_name + "_args"] = variables

# switches to window
def switch_to_window(window_name, callback=None):
    global activeWindow

    if activeWindow is not None:
        activeWindow.destroy()

    root = tk.Tk()
    activeWindow = root

    args = (root,) + windows[window_name](*args)

    frame.grid(row=0, column=0)

    if callback:
        callback(frame)
    root.mainloop()