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

master.grid_rowconfigure(0, weight=1)
master.grid_rowconfigure(7, weight=1)
master.grid_columnconfigure(0, weight=1)
master.grid_columnconfigure(7, weight=1)

frame = tk.Frame(master, width=1000, height=600, bg="white")
frame.grid(row=0, column=0)
#frame.eval('tk::PlaceWindow . center')

cal = Calendar(frame, selectmode='day', year=2020, month=5, day=22)
cal.grid(row=1, column=3)

display = tk.Frame(frame, bg="black", width=500, height=300)
display.grid(row=1, column=0, columnspan=3)

def hide_widget(widget):
    widget.pack_forget()

def show_widget(widget):
    widget.pack()

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())

date = tk.Label(frame, text="")
date.grid(row=2, column=3)

figure1 = plt.Figure(figsize=(3,2), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, frame)
bar1.get_tk_widget().grid(row=3, column=3)
#bar1.get_tk_widget().pack()
#bar1.get_tk_widget().place(x=300, y=700)
df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Country Vs. GDP Per Capita')

lbl_dur = tk.Label(frame, bg="gray", width=30, height=7)
lbl_dur.grid(row=0, column=0, padx=20, pady=20)

lbl_status = tk.Label(frame, bg="gray", width=30, height=7)
lbl_status.grid(row=0, column=1, padx=20, pady=20)

lbl_rate = tk.Label(frame, bg="gray", width=30, height=7)
lbl_rate.grid(row=0, column=2, padx=20, pady=20)

#fileName = "sample.gif"
#file_name = tk.PhotoImage(file=fileName)
#canvas = tk.Canvas()
#display = tk.Frame(master, bg="blue", width=100, height=100)
#display.pack()
#display.place(x=50, y=350)
#canvas.create_image(100, 100, anchor='nw', image=file_name)

btn_settings = tk.Button(frame, text="Settings", width=20, height=3)
btn_settings.grid(row=3, column=0)

btn_show = tk.Button(frame, text="SHOW VISION", command=lambda:display.pack_forget(), width=25, height=3)
btn_show.grid(row=3, column=1)

btn_notif = tk.Button(frame, text="Notifications", width=20, height=3)
btn_notif.grid(row=3, column=2)

master.mainloop()
