
import cv2
import sys
import os
from imutils.video import FPS


class doorBellApp():
    def __init__(self):
        
        self.inname = ''
        self.exname = []
        ###########
        devs = os.listdir('/dev')
        self.v = [int(dev[-1]) for dev in devs if dev.startswith('video')]
        self.v = sorted(self.v)
        #print(self.v)
        '''                   '''
        devs = os.listdir('/dev')
        self.v = []
        for dev in devs:
            if dev.startswith('video'):
                self.v.append(int(dev[-1]))
            self.exname.append(dev)
        ############
        self.d = 0
        self.ava_dev = []
        searching = True
        while searching:
            self.cam = cv2.VideoCapture(self.d)
            ret, _ = self.cam.read()
            if not ret:
                break
            else:
                self.ava_dev.append(self.d)
                if self.d == 0:
                    self.inname = sys.platform.capitalize()
                    searching = False
                self.exname = []
            self.d += 1

        self.cam.read()
        if len(self.ava_dev) == 0:
            raise Exception('Something Went Wrong! ' +
                            sys.platform.capitalize() +
                            ' DEVICE COULD NOT CONNECT TO A CAMERA.')
    def read(self):
        return self.cam.read()

    def available_dev(self):
        return self.ava_dev

    def name(self):
        return self.v#['h', 'd']

    def set(self):
        return cv2.VideoCapture(0)

    def destroy(self):
        cv2.destroyAllWindows()

    def release(self):
        self.cam.release()


