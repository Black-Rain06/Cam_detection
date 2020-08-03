import cv2
import numpy as np
import imutils
import time
import sys
import numpy

from imutils.video import FPS


running = True

class doorBellCam():

    
    def __init__(self, title):

        self.title = title

        self.paused = False
        self.cap = cv2.VideoCapture(0)
        fps = FPS().start()
        
        self.fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        self.out = cv2.VideoWriter("output.avi", self.fourcc, 5.0, (480,480))
        
        ret, frame1 = self.cap.read()

        while self.cap.isOpened() and not self.paused:
            
            _, frame2 = self.cap.read()
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            erode = cv2.erode(thresh.copy(), None, iterations=10)
            dilated = cv2.dilate(erode, None, iterations=10)
            contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) != 0:
                c = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame1,(x,y),(x+w*2,y+h*2),(0,0,255),2)
                cv2.rectangle(frame2,(x,y),(x+w*2,y+h*2),(0,255,0),2)
                print('Detected Motion')
            else:
                print('No motion or motion insignificant')

            self.image = imutils.resize(frame2, width=850)
            self.out.write(self.image)
            cv2.imshow(self.title, self.image)
            frame1 = frame2

            fps.update()

            key = cv2.waitKey(20)

            if key == ord('q'):
                running = False
                self.freeSpace()
                sys.exit()
                break

            if key == ord('m'):
                self.paused = True
                cv2.imshow(self.title, self.image)
                if key == ord('q'):
                    running = False
                    self.freeSpace()
                    sys.exit()
                    break

            
    def resume(self):
        self.paused = False


    def freeSpace(self):

        cv2.destroyAllWindows()
        cv2.destroyAllWindows()
        self.cap.release()
        self.out.release()

