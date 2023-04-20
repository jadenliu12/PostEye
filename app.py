import tkinter as tk
import tkinter
from tkcalendar import Calendar
import cv2
import dlib
from PIL import Image, ImageTk
from numpy.linalg import norm
import screen_brightness_control as sbc

from datetime import date, datetime, timedelta
import math
import numpy as np
import pandas as pd

from model import binary_relevance

# Initiate detector
detector = dlib.get_frontal_face_detector()

# Hyper Variables
BLINK_RATIO_THRESHOLD = 5.7
counter_min = 0
counter_hrs = 0
key = 0
toggle = 0
token = 0
theme = "white"
count = 0
brightness_val = 0
counter = 0
minute = 0
hour = 0

# Load Assets
bg_img = Image.open("./assets/eye.png")
url = "./data/Posteye_data.csv"

def save():
    global my_records
    with open('records.txt', 'w') as fh:
        fh.write('\n'.join(rec for rec in my_records))

def brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)

class GradientFrame(tk.Canvas): # to make color gradient frames
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="red", color2="black", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")

class Notification:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.frame = tk.Frame(self.window, width=300, height=500, bg="white")
        self.frame.grid(row=0, column=0)
        
        self.alarm_on = tk.IntVar()
        self.alarm_off = tk.IntVar()

        self.label_alarm = tk.Label(self.frame, text="Alarm Notifications")
        self.label_alarm.grid(row=0, column=0, columnspan=2)

        self.alarm_on_check = tk.Checkbutton(self.frame, text="On", variable=self.alarm_on, onvalue=1, offvalue=0, height=5, width=20)
        self.alarm_on_check.grid(row=1, column=0)

        self.alarm_off_check = tk.Checkbutton(self.frame, text="Off", variable=self.alarm_off, onvalue=1, offvalue=0, height=5, width=20)
        self.alarm_off_check.grid(row=1, column=1)


        self.sleep_on = tk.IntVar()
        self.sleep_off = tk.IntVar()

        self.label_sleep = tk.Label(self.frame, text="Auto-Sleep Laptop")
        self.label_sleep.grid(row=2, column=0, columnspan=2)

        self.sleep_on_check = tk.Checkbutton(self.frame, text="On", variable=self.sleep_on, onvalue=1, offvalue=0, height=5, width=20)
        self.sleep_on_check.grid(row=3, column=0)

        self.sleep_off_check = tk.Checkbutton(self.frame, text="Off", variable=self.sleep_off, onvalue=1, offvalue=0, height=5, width=20)
        self.sleep_off_check.grid(row=3, column=1)
        
        self.app_on = tk.IntVar()
        self.app_off = tk.IntVar()

        self.label_app = tk.Label(self.frame, text="Application Notifications")
        self.label_app.grid(row=4, column=0, columnspan=2)

        self.app_on_check = tk.Checkbutton(self.frame, text="On", variable=self.app_on, onvalue=1, offvalue=0, height=5, width=20)
        self.app_on_check.grid(row=5, column=0)

        self.app_off_check = tk.Checkbutton(self.frame, text="Off", variable=self.app_off, onvalue=1, offvalue=0, height=5, width=20)
        self.app_off_check.grid(row=5, column=1)

        self.btn_home = tk.Button(self.frame, text="Home")
        self.btn_home.grid(row=6, column=0, columnspan=2)

class Settings:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.frame = tk.Frame(self.window, width=300, height=500, bg="white")
        self.frame.grid(row=0, column=0)
        
        self.alarm_on = tk.IntVar(value = 1)
        self.alarm_off = tk.IntVar()

        self.label_alarm = tk.Label(self.frame, text="Automatic Brightness Adjustment")
        self.label_alarm.grid(row=0, column=0, columnspan=2)

        self.alarm_on_check = tk.Checkbutton(self.frame, text="On", variable=self.alarm_on, onvalue=1, offvalue=0, height=5, width=20)
        self.alarm_on_check.grid(row=1, column=0)

        self.alarm_off_check = tk.Checkbutton(self.frame, text="Off", variable=self.alarm_off, onvalue=1, offvalue=0, height=5, width=20)
        self.alarm_off_check.grid(row=1, column=1)

        self.sleep_on = tk.IntVar(value = 1)
        self.sleep_off = tk.IntVar()

        self.label_sleep = tk.Label(self.frame, text="Blink Detection")
        self.label_sleep.grid(row=2, column=0, columnspan=2)

        self.sleep_on_check = tk.Checkbutton(self.frame, text="On", variable=self.sleep_on, onvalue=1, offvalue=0, height=5, width=20)
        self.sleep_on_check.grid(row=3, column=0)

        self.sleep_off_check = tk.Checkbutton(self.frame, text="Off", variable=self.sleep_off, onvalue=1, offvalue=0, height=5, width=20)
        self.sleep_off_check.grid(row=3, column=1)
        
        global token
        if token == 1:
            self.app_on = tk.IntVar()
            self.app_off = tk.IntVar(1)
        else:
            self.app_on = tk.IntVar(1)
            self.app_off = tk.IntVar()

        self.label_app = tk.Label(self.frame, text="Theme")
        self.label_app.grid(row=4, column=0, columnspan=2)

        self.app_on_check = tk.Checkbutton(self.frame, text="Light", variable=self.app_on, onvalue=1, offvalue=0, height=5, width=20)
        self.app_on_check.grid(row=5, column=0)

        self.app_off_check = tk.Checkbutton(self.frame, text="Dark", variable=self.app_off, onvalue=1, offvalue=0, height=5, width=20)
        self.app_off_check.grid(row=5, column=1)

        self.btn_home = tk.Button(self.frame, text="Home")
        self.btn_home.grid(row=6, column=0, columnspan=2)



class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(7, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(7, weight=1)
        
        # self.frame = tk.Frame(self.window, width=1000, height=1500, bg="white")
        # self.frame.grid(row=0, column=0)

        self.frame = tk.Frame(self.window, width=1200, height=1000, bg= "white")
        self.frame.grid(row=1, column=0, padx=1)

        self.canvas1 = GradientFrame(self.frame, "#00F4FF", "#00F3B9", width = 1300, height = 100, relief="ridge")
        self.canvas1.grid(row=0, column=0 ,columnspan=4)

        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)

        self.canvas = tkinter.Canvas(self.frame, width = 600, height = 400)
        self.canvas.grid(row=2, column=0, columnspan=3, rowspan = 3)

        todays_date = date.today()
        self.year = int(todays_date.year)
        self.month = int(todays_date.month)
        self.day = int(todays_date.day)
        self.cal = Calendar(self.frame, selectmode='day', year=self.year, month=self.month, day=self.day)
        self.cal.grid(row=2, column=3)

        self.date = tk.Label(self.frame, text="")
        self.date.grid(row=3, column=3)
        
        self.minimize = tk.Button(self.frame, text="Minimize", command=lambda: self.toggle_window())
        self.minimize.grid(row=1, column=3)

        #self.figure1 = plt.Figure(figsize=(3,2), dpi=100)
        #self.ax1 = self.figure1.add_subplot(111)
        #self.bar1 = FigureCanvasTkAgg(self.figure1, self.frame)
        #self.bar1.get_tk_widget().grid(row=3, column=3)
        #bar1.get_tk_widget().pack()
        #bar1.get_tk_widget().place(x=300, y=700)
        #self.df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
        #self.df1.plot(kind='bar', legend=True, ax=self.ax1)
        #self.ax1.set_title('Country Vs. GDP Per Capita')

        self.lbl_dur = tk.Label(self.frame, bg="white", borderwidth=2, width=30, height=7, relief="groove", fg="black")
        self.lbl_dur.grid(row=1, column=0, padx=20, pady=20)

        self.lbl_status = tk.Label(self.frame, bg="white", borderwidth=2, width=30, height=7, relief="groove", fg="black")
        self.lbl_status.grid(row=1, column=1, padx=20, pady=20)

        self.lbl_rate = tk.Label(self.frame, bg="white", borderwidth=2, width=30, height=7, relief="groove", fg="black")
        self.lbl_rate.grid(row=1, column=2, padx=20, pady=20)

        self.btn_settings = tk.Button(self.frame, text="Settings", command = lambda: self.change_color(), width=20, height=3)
        self.btn_settings.grid(row=5, column=0, pady = 20)

        self.btn_show = tk.Button(self.frame, text="SHOW VISION", command = lambda: self.change_cam(), width=25, height=3)
        self.btn_show.grid(row=5, column=1, pady = 20)

        self.btn_notif = tk.Button(self.frame, text="Notifications", command = lambda: self.on_click_notification(), width=20, height=3)
        self.btn_notif.grid(row=5, column=2, pady = 20)

        self.btn_data = tk.Button(self.frame, text="Get Data", command = lambda: self.selected_date(), width=20, height=3)
        self.btn_data.grid(row=5, column=3, pady = 20)

        self.dataset = pd.read_csv(url)
        self.br = binary_relevance(url, self.dataset)
        self.X_train, self.X_test, self.y_train, self.y_test = self.br.split_data()
        
        self.delay = 15
        self.ts = datetime.now()
        self.update()

        self.window.mainloop()

    def update(self):
        global bg_img, counter_min, counter_hrs, timer_min, timer_hrs, brightness_val, minute, hour, count, counter
        ret, frame = self.vid.get_frame()
        cv2.putText(frame,"BLINKING : " + str(counter_min),(10,50), cv2.FONT_HERSHEY_SIMPLEX,
                     2,(255,255,255),2,cv2.LINE_AA)
        
        if ret:
            if key == 0:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            else:
                self.photo = ImageTk.PhotoImage(bg_img)
                self.canvas.create_image(300, 200, image = self.photo, anchor = tkinter.CENTER)
        
        self.lbl_rate.config(text = "{cnt:.2f} blinks/mins".format(cnt = timer_min.get_count()/60))
        self.lbl_dur.config(text = "{cnt} seconds \n {mnt} minutes \n {hr} hours".format(cnt = count, mnt = minute, hr = hour))
        self.window.after(self.delay, self.update)

        count = count + 1
        now = datetime.now()
        diff = now - self.ts
        diff_in_s = int(diff.total_seconds())

        count = diff_in_s % 60
        minute = diff_in_s // 60
        hour = diff_in_s // 3600

        if timer_min.is_minute():
            counter_min = 0
        elif timer_hrs.is_hour():
            counter_hrs = 0
                        
        if counter%5 ==0:
            if brightness_val > 100:
                sbc.set_brightness(50, display = 0)
            else:
                sbc.set_brightness(65, display=0)
        counter = counter + 1

        if(timer_min.is_minute):
            rate = timer_min.get_prev_blink()
            pred = self.br.predict(np.array(rate).reshape(-1,1))
            text = ''
            if minute >= 1:
                if(pred[0][0] == 1 and pred[0][1] == 1):
                    text = "Asleep or Tired"
                elif(pred[0][0] == 1 and pred[0][1] == 0):
                    text = "Tired"
                elif(pred[0][0] == 0 and pred[0][1] == 1):
                    text = "Sleepy"
                elif(pred[0][0] == 0 and pred[0][1] == 0):
                    text = "Normal"
            else:
                text = "Wait for the 1st one minute"
            self.lbl_status.config(text = text)

    def change_cam(self):
        global key
        if key == 0:
            key = 1
        else: 
            key = 0
            
    def selected_date(self):
        print("Selected Date is: " + self.cal.get_date())

    def change_color(self):
        global token
        if token == 0:
            self.frame.config(bg="#626262")
            self.lbl_dur.config(bg="#393E46", fg="white")
            self.lbl_status.config(bg="#393E46", fg="white")
            self.lbl_rate.config(bg="#393E46", fg="white")
            self.canvas1 = GradientFrame(self.frame, "#00F4FF", "#2187FF", width = 1300, height = 100, relief="ridge")
            self.canvas1.grid(row=0, column=0 ,columnspan=4)
            token = 1
        else:
            self.frame.config(bg="white")
            self.lbl_dur.config(bg="white", fg="black")
            self.lbl_status.config(bg="white", fg="black")
            self.lbl_rate.config(bg="white", fg="black")
            self.canvas1 = GradientFrame(self.frame, "#00F4FF", "#00F3B9", width = 1300, height = 100, relief="ridge")
            self.canvas1.grid(row=0, column=0 ,columnspan=4)
            token = 0

    def on_click_notification(self):
        Notification(tk.Toplevel(), "Notification Settings")

    def on_click_settings(self):
        Settings(tk.Toplevel(), "Notification Settings")

    def toggle_window(self):
        minim = Minimized(tk.Toplevel(), "Posteye")
        self.window.withdraw()
        
    def show(self):
        self.window.deiconify()    

class Minimized:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.window.geometry('364x150+100+69')
        self.window.resizable(0, 0)
        self.window.resizable(False, False)
        self.window.iconbitmap('./assets/eye_icon.ico')
        
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

    def toggle_window(self):
        app.show()
        self.window.iconify()

    def showandhide(self):
        self.window.iconify()

class Timer:
    def __init__(self, start, duration, blink_no):
        self.start = start
        self.duration = duration #in seconds
        self.blink_no = blink_no
        self.prev_blink = 0
        self.records = []
        self.cur_time = datetime.now()

    def get_records(self):
        return self.records

    def get_count(self):
        return self.blink_no

    def get_timer(self):
        return self.cur_time

    def get_prev_blink(self):
        return self.prev_blink

    def set_timer(self, time):
        self.cur_time = time

    def update_blink(self):
        if self.duration == 3600:
            if (self.cur_time) >= (self.start + timedelta(seconds=self.duration)):
                now = str(datetime.now())
                no_blink = str(self.blink_no)
                insert = now + ' ' + no_blink
                self.records.append(insert)
                self.prev_blink = self.blink_no
                self.blink_no = 0
                self.start = datetime.now()
                return 0
            else:
                self.blink_no += 1
        else:
            print((self.cur_time) >= (self.start + timedelta(seconds=60)))
            print(self.cur_time)
            print(self.start + timedelta(seconds=60))
            if (self.cur_time) >= (self.start + timedelta(seconds=60)):
                self.prev_blink = self.blink_no
                self.blink_no = 0
                self.start = datetime.now()
                return 0
            else:
                self.blink_no += 1
        return self.blink_no

    def is_minute(self):
        if (self.cur_time) >= (self.start + timedelta(seconds=60)):
            return True
        else:
            return False

    def is_hour(self):
        if (self.cur_time) >= (self.start + timedelta(seconds=3600)):
            return True
        else:
            return False

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        global first_execute_min,  first_execute_hrs, one_min, one_hrs
        if self.vid.isOpened():
            self.vid.set(3, 480)
            self.vid.set(4, 360)
            self.vid.set(15, 0.1)
            ret, frame = self.vid.read()
            global detector, counter_min, counter_hrs
            predictor = dlib.shape_predictor("./data/shape_predictor_68_face_landmarks.dat")
            left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
            right_eye_landmarks = [42, 43, 44, 45, 46, 47]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces,_,_ = detector.run(image = gray, upsample_num_times = 0, adjust_threshold = 0.0)

            for face in faces:
                
                landmarks = predictor(gray, face)

                left_eye_ratio  = self.get_blink_ratio(left_eye_landmarks, landmarks)
                right_eye_ratio = self.get_blink_ratio(right_eye_landmarks, landmarks)
                blink_ratio     = (left_eye_ratio + right_eye_ratio) / 2

                if not timer_min.is_minute():
                    timer_min.set_timer(datetime.now())
                if not timer_hrs.is_hour():
                    timer_hrs.set_timer(datetime.now())
                
                if blink_ratio > BLINK_RATIO_THRESHOLD:
                    counter_min = timer_min.update_blink()
                    counter_hrs = timer_hrs.update_blink()

            ret, frame = self.vid.read()
            global brightness_val
            brightness_val = brightness(frame)
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

    def midpoint(self, point1 ,point2):
        return (point1.x + point2.x)/2,(point1.y + point2.y)/2
    
    def euclidean_distance(self, point1 , point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def get_blink_ratio(self, eye_points, facial_landmarks):
        corner_left  = (facial_landmarks.part(eye_points[0]).x, 
                        facial_landmarks.part(eye_points[0]).y)
        corner_right = (facial_landmarks.part(eye_points[3]).x, 
                        facial_landmarks.part(eye_points[3]).y)
        
        center_top    = self.midpoint(facial_landmarks.part(eye_points[1]), 
                                 facial_landmarks.part(eye_points[2]))
        center_bottom = self.midpoint(facial_landmarks.part(eye_points[5]), 
                                 facial_landmarks.part(eye_points[4]))

        horizontal_length = self.euclidean_distance(corner_left,corner_right)
        vertical_length = self.euclidean_distance(center_top,center_bottom)

        ratio = horizontal_length / vertical_length

        return ratio
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

cv2.setUseOptimized(True)
first_execute_min = datetime.now() 
first_execute_hrs = datetime.now()
one_min = 60
one_hrs = 3600
timer_min = Timer(first_execute_min, one_min, counter_min)
timer_hrs = Timer(first_execute_hrs, one_hrs, counter_hrs)
my_records = timer_hrs.get_records()
app = App(tkinter.Tk(), "POSTEYE")
save()
