from datetime import date
import cv2
import dlib
import math
from PIL import Image, ImageTk
from datetime import datetime
BLINK_RATIO_THRESHOLD = 5.7

detector = dlib.get_frontal_face_detector()
counter_min = 0
counter_hrs = 0
key = 0
toggle = 0
token = 0
bg_img = Image.open("./eye.png")
theme = "white"

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
right_eye_landmarks = [42, 43, 44, 45, 46, 47]

first_execute_min = datetime.now() 
first_execute_hrs = datetime.now()
one_min = 60
one_hrs = 3600

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.vid.set(cv2.CAP_PROP_POS_MSEC, 1000)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        global first_execute_min, first_execute_hrs, one_min, one_hrs, left_eye_landmarks, right_eye_landmarks
        if self.vid.isOpened():
            self.vid.set(3, 480)
            self.vid.set(4, 360)
            self.vid.set(15, 0.1)
            ret, frame = self.vid.read()
            global detector, counter_min, counter_hrs
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces,_,_ = detector.run(image = gray, upsample_num_times = 0, adjust_threshold = 0.0)

            for face in faces:
                
                landmarks = predictor(gray, face)

                left_eye_ratio  = self.get_blink_ratio(left_eye_landmarks, landmarks)
                right_eye_ratio = self.get_blink_ratio(right_eye_landmarks, landmarks)
                blink_ratio     = (left_eye_ratio + right_eye_ratio) / 2

                first_execute_min = datetime.now() if timer_min.is_minute() else first_execute_min 
                first_execute_hrs = datetime.now() if timer_hrs.is_hour() else first_execute_hrs

                if blink_ratio > BLINK_RATIO_THRESHOLD:
                    counter_min = timer_min.update_blink()
                    counter_hrs = timer_hrs.update_blink()

            ret, frame = self.vid.read()
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