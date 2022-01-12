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
from Minimized import *
from app import *



application = App(tkinter.Tk(), "POSTEYE")
minim = Minimized(tk.Toplevel(), "Posteye")


def helohelo():
    if application.ispressed() == True:
        application.hide()
        minim.show()
