import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from tkcalendar import Calendar

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pandas import DataFrame

###############################DUMMY DATA############################################
data1 = {'Country': ['US','CA','GER','UK','FR'],
         'GDP_Per_Capita': [45000,42000,52000,49000,47000]
        }
df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])


data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        }
df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])


data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
         'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
        }  
df3 = DataFrame(data3,columns=['Interest_Rate','Stock_Index_Price'])
#####################################################################################

master = tk.Tk()
master.title("POSTEYE")

frame = tk.Frame(master, width=1000, height=600, bg="white")
frame.pack_propagate(0)
frame.pack()

cal = Calendar(master, selectmode='day', year=2020, month=5, day=22)
cal.pack(pady=20)
cal.place(x=665, y=200)

display = tk.Frame(master, bg="black", width=500, height=300)
display.pack()
display.place(x=50, y=200)

def hide_widget(widget):
    widget.pack_forget()

def show_widget(widget):
    widget.pack()

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())

date = tk.Label(master, text="")
date.pack(pady=20)

figure1 = plt.Figure(figsize=(3,2), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, master)
bar1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
#bar1.get_tk_widget().pack()
#bar1.get_tk_widget().place(x=300, y=700)
df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Country Vs. GDP Per Capita')

lbl_dur = tk.Label(master, bg="gray", borderwidth=1,  width=30, height=7)
lbl_dur.pack()
lbl_dur.place(x=50, y=30)

lbl_status = tk.Label(master, bg="gray", width=30, height=7)
lbl_status.pack()
lbl_status.place(x=375, y=30)

lbl_rate = tk.Label(master, bg="gray", width=30, height=7)
lbl_rate.pack()
lbl_rate.place(x=700, y=30)

#fileName = "sample.gif"
#file_name = tk.PhotoImage(file=fileName)
#canvas = tk.Canvas()
#display = tk.Frame(master, bg="blue", width=100, height=100)
#display.pack()
#display.place(x=50, y=350)
#canvas.create_image(100, 100, anchor='nw', image=file_name)

btn_settings = tk.Button(master, text="Settings", width=20, height=3)
btn_settings.pack()
btn_settings.place(x=50, y=550)

btn_show = tk.Button(master, text="SHOW VISION", command=lambda:display.pack_forget(), width=25, height=3)
btn_show.pack()
btn_show.place(x=250, y=550)

btn_notif = tk.Button(master, text="Notifications", width=20, height=3)
btn_notif.pack()
btn_notif.place(x=495, y=550)

master.mainloop()
