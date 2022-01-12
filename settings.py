import tkinter as tk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(7, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(7, weight=1)

        self.window.mainloop()
        
App(tk.Tk(), "Settings")
