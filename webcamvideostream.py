import cv2
from threading import Thread
import time
import numpy as np

class WebcamVideoStream:
    def __init__(self, src = 0):
        print("init")
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        time.sleep(2.0)
    
    def start(self):
        print("start thread")
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        print("read")
        while True:
            if self.stopped:
                return
            
            (self.grabbed, self.frame) = self.stream.read()
            
            gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)

            ret,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
            erode = cv2.erode(thresh, None, iterations=10)
            dilated = cv2.dilate(erode, None, iterations=10)

            contours, hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            
            for contour in contours:
                if cv2.contourArea(contour) < 10000:
                    (x,y,w,h) = cv2.boundingRect(contour)
                    cv2.rectangle(self.frame, (x,y), (x+w, y+h), (0,255,0), 3)
    
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True

