import time
import cv2
import numpy as np
from imutils.video import VideoStream
import imutils


usingPiCamera = True

fs = (320, 240)

vs = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=fs,
		framerate=32).start()

time.sleep(2.0)

timeCheck = time.time()

class Chyme():

    def __init __(self):
        
        while True:
            self.frame = vs.read()
            
            if not usingPiCamera:
                    frame = imutils.resize(self.frame, width=fs[0])
     
            cv2.imshow('orig', self.frame)
            key = cv2.waitKey(1) & 0xFF
     
            if key == ord("q"):
                    break
        cv2.destroyAllWindows()
        vs.stop()


def main():
    c = Chyme()
    return c

main()

'''timeCheck = time.time()'''
