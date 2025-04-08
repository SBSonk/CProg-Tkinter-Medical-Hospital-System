import tkinter as tk
from tkinter import ttk

# An entry box with a placeholder
class PlaceholderEntry(ttk.Entry):
    disabled = False
    placeholder_text = ""
    is_password = False

    normal_font = ()
    text_color='black'
    placeholder_font = ()
    placeholder_color='gray'

    def focus_in(self, event):
        if self.disabled:
            return
        
        if self.get() == self.placeholder_text:
            self.delete(0, 'end')
            self.configure(font=self.normal_font, foreground=self.text_color)

            if self.is_password:
                self.configure(show="*")
    def focus_out(self, event):
        if self.disabled:
            return
        
        if self.get() == "":
            self.insert(0, self.placeholder_text)
            self.configure(foreground=self.placeholder_color)

            if self.is_password:
                self.configure(show="")
    
    def get_text(self):
        text = super().get()
        
        if text == self.placeholder_text:
            text = ""
        return text

    def set_disabled(self, val):
        self.disabled = val
        if val:
            self.delete(0, 'end')
            self.insert(0, 'Disabled')
            
            self.config(state='disabled')
        else:
            self.config(state='normal')
            
            self.delete(0, 'end')
            self.insert(0, self.placeholder_text)
            self.configure(foreground=self.placeholder_color)
            
            if self.is_password:
                self.configure(show="")
                
            

    def __init__(self, master = None, normal_font=('Arial', 12), text_color='black', placeholder_font=('Arial', 12), placeholder_color='gray', placeholder_text="", is_password = False, width=20):
        super().__init__(master, font=normal_font, foreground=text_color, width=width)
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.placeholder_text = placeholder_text
        self.placeholder_font = placeholder_font
        self.normal_font = normal_font
        self.is_password = is_password
        
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

        self.focus_out(lambda: _)

# Label with color changes on hover
class HyperlinkLabel(ttk.Label):
    default_color = ''
    hover_color = ''

    def on_hover(self, event):
        self.configure(foreground=self.hover_color)

    def on_hover_end(self, event):
        self.configure(foreground=self.default_color)

    def __init__(self, master, text, on_click, default_color='black', hover_color='black'):
        super().__init__(master, text=text, foreground=default_color)
        self.default_color = default_color

        self.bind('<Button-1>', on_click)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_hover_end)