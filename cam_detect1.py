#Cam_detect.py

from imutils.video import FPS

import cv2 as cv
import numpy as np
import imutils


cap = cv.VideoCapture(0)

while(True):

    ret, grayframe = cap.read()

    if not ret:
        break

    grayframe = imutils.resize(grayframe, width=850)
    grayframe = cv.cvtColor(grayframe, cv.COLOR_BGR2GRAY)
    grayframe = np.dstack([grayframe, grayframe, grayframe])


    cv.putText(grayframe, 'Cam 01', (10,30),
               cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

    cv.imshow('frame', grayframe)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    fps = FPS().start()
    fps.update()

cap.release()
cv.destroyAllWindows()

