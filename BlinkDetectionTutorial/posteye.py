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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
BLINK_RATIO_THRESHOLD = 5.7

#-----Step 3: Face detection with dlib-----
detector = dlib.get_frontal_face_detector()
counter = 0
key = 0
bg_img = Image.open("./eye.png")

#-----Step 4: Detecting Eyes using landmarks in dlib-----
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#these landmarks are based on the image above 
left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
right_eye_landmarks = [42, 43, 44, 45, 46, 47]

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
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(7, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(7, weight=1)
        
        self.frame = tk.Frame(self.window, width=1000, height=600, bg="white")
        self.frame.grid(row=0, column=0)

        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.frame, width = 500, height = 300)
        self.canvas.grid(row=1, column=0, columnspan=3)
        
        self.cal = Calendar(self.frame, selectmode='day', year=2020, month=5, day=22)
        self.cal.grid(row=1, column=3)

        self.date = tk.Label(self.frame, text="")
        self.date.grid(row=2, column=3)

        self.figure1 = plt.Figure(figsize=(3,2), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.frame)
        self.bar1.get_tk_widget().grid(row=3, column=3)
        #bar1.get_tk_widget().pack()
        #bar1.get_tk_widget().place(x=300, y=700)
        self.df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
        self.df1.plot(kind='bar', legend=True, ax=self.ax1)
        self.ax1.set_title('Country Vs. GDP Per Capita')

        self.lbl_dur = tk.Label(self.frame, bg="gray", width=30, height=7)
        self.lbl_dur.grid(row=0, column=0, padx=20, pady=20)

        self.lbl_status = tk.Label(self.frame, bg="gray", width=30, height=7)
        self.lbl_status.grid(row=0, column=1, padx=20, pady=20)

        self.lbl_rate = tk.Label(self.frame, bg="gray", width=30, height=7)
        self.lbl_rate.grid(row=0, column=2, padx=20, pady=20)

        self.btn_settings = tk.Button(self.frame, text="Settings", width=20, height=3)
        self.btn_settings.grid(row=3, column=0)

        self.btn_show = tk.Button(self.frame, text="SHOW VISION", width=25, height=3)
        self.btn_show.grid(row=3, column=1)

        self.btn_notif = tk.Button(self.frame, text="Notifications", width=20, height=3)
        self.btn_notif.grid(row=3, column=2)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

    # def grad_date():
    #     date.config(text="Selected Date is: " + self.cal.get_date())


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()

            detector = dlib.get_frontal_face_detector()
            counter = 0
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
            #these landmarks are based on the image above 
            left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
            right_eye_landmarks = [42, 43, 44, 45, 46, 47]

            #-----Step 2: converting image to grayscale-----
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #-----Step 3: Face detection with dlib-----
            #detecting faces in the frame 
            faces,_,_ = detector.run(image = gray, upsample_num_times = 0, adjust_threshold = 0.0)

            cv2.putText(frame,"BLINKING : " + str(counter),(10,50), cv2.FONT_HERSHEY_SIMPLEX,
                    2,(255,255,255),2,cv2.LINE_AA)

            #-----Step 4: Detecting Eyes using landmarks in dlib-----
            for face in faces:
                
                landmarks = predictor(gray, face)

                #-----Step 5: Calculating blink ratio for one eye-----
                left_eye_ratio  = self.get_blink_ratio(left_eye_landmarks, landmarks)
                right_eye_ratio = self.get_blink_ratio(right_eye_landmarks, landmarks)
                blink_ratio     = (left_eye_ratio + right_eye_ratio) / 2

                if blink_ratio > BLINK_RATIO_THRESHOLD:
                    #Blink detected! Do Something!
                    counter = counter + 1

            #cv2.imshow('BlinkDetector', frame)

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        # else:
        #     return (ret, None)

    #-----Step 5: Getting to know blink ratio
    def midpoint(self, point1 ,point2):
        return (point1.x + point2.x)/2,(point1.y + point2.y)/2

    def euclidean_distance(self, point1 , point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def get_blink_ratio(self, eye_points, facial_landmarks):
        
        #loading all the required points
        corner_left  = (facial_landmarks.part(eye_points[0]).x, 
                        facial_landmarks.part(eye_points[0]).y)
        corner_right = (facial_landmarks.part(eye_points[3]).x, 
                        facial_landmarks.part(eye_points[3]).y)
        
        center_top    = self.midpoint(facial_landmarks.part(eye_points[1]), 
                                facial_landmarks.part(eye_points[2]))
        center_bottom = self.midpoint(facial_landmarks.part(eye_points[5]), 
                                facial_landmarks.part(eye_points[4]))

        #calculating distance
        horizontal_length = self.euclidean_distance(corner_left,corner_right)
        vertical_length = self.euclidean_distance(center_top,center_bottom)

        ratio = horizontal_length / vertical_length

        return ratio


     # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

App(tkinter.Tk(), "POSTEYE")
