import cv2
from threading import Thread
import time
import numpy as np

class WebcamVideoStream:
    def __init__(self, src = 0):
        print("init")
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        (self.grabbed1, self.frame1) = self.stream.read()
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
            (self.grabbed, self.frame) = self.stream.read()
            (self.grabbed1, self.frame1) = self.stream.read()
            diff = cv2.absdiff(self.frame, self.frame1)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            erode = cv2.erode(thresh.copy(), None, iterations=5)
            dilated = cv2.dilate(erode, None, iterations=5)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                c = max(contours, key = cv2.contourArea)
                (x, y, w, h) = cv2.boundingRect(c)


                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(self.frame, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)                                                                    
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True

