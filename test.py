import tkinter as tk

root = tk.Tk()

root.title('Tkinter Window Demo')
root.geometry('364x150+1000+690')
root.resizable(0, 0)
root.resizable(False, False)
root.iconbitmap('./eye_icon.ico')

root.mainloop()
