import tkinter as tk

windows = {}
activeWindow = None

# use this to add a window that can be switched to
def add_window(window_name, frame: tk.Frame, init_args: tuple = ()): 
    windows[window_name] = frame
    windows[window_name + "_args"] = init_args

# switches to window
def switch_to_window(window_name, callback=None, onCreateArgs: tuple = ()): 
    global activeWindow

    if activeWindow is not None:
        activeWindow.destroy()

    root = tk.Tk()
    activeWindow = root

    args = (root,) + windows[window_name + "_args"]
    frame: tk.Frame = windows[window_name](*args + onCreateArgs)

    frame.grid(row=0, column=0)

    if callback:
        callback(frame)
        
    root.mainloop()

    