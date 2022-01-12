import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from tkcalendar import Calendar
import tkinter
import cv2
import dlib
import math
from PIL import Image, ImageTk
import time
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from threading import Thread

class Minimized:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.window.geometry('364x150+100+69')
        self.window.resizable(0, 0)
        self.window.resizable(False, False)
        self.window.iconbitmap('./eye_icon.ico')
        
        self.frame = tk.Frame(self.window, width=364, height=150, bg= "#626262")
        self.frame.grid(row=0, column=0)
        
        self.canvas1 = tk.Frame(self.frame, width = 364, height=30, bg= "#00F4FF")
        self.canvas1.grid(row=0, column=0 ,columnspan=4)

        #temp = ImageTk.PhotoImage(Image.open("./eye_color.png"))
        #self.img = tk.Label(self.canvas1, image = temp, height=6)
        #self.img.pack()  

        self.lbl_dur = tk.Label(self.canvas1, text="hello", bg= "#00F4FF", height=4, font=('Arial', 11))
        self.lbl_dur.grid(row=0, column=0, padx = 50)

        self.lbl_status = tk.Label(self.canvas1, text="hello", bg= "#00F4FF", height=4, font=('Arial', 11))
        self.lbl_status.grid(row=0, column=1, padx = 50)

        self.lbl_rate = tk.Label(self.canvas1, text="hello", bg= "#00F4FF", height=4, font=('Arial', 11))
        self.lbl_rate.grid(row=0, column=2, padx = 50)

        self.btn_maximize = tk.Button(self.canvas1, text="Maximize", command=lambda: self.toggle_window())
        self.btn_maximize.grid(row=1, column=0)

        self.hide()
        

    def toggle_window(self):
        self.hide()

    def hide(self):
        self.window.iconify()

    def show(self):
        self.window.deiconify()



