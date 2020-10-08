# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from imutils.video import FPS

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from kivy.properties import*

from doorBellApp import doorBellApp


from datetime import datetime
import kivy 
import cv2
import numpy as np
import bluetooth
import imutils
import sys


notify = {'No records':'',}

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        #self.notify
    
    def update(self, dt):
        fps = FPS().start()
        self.frame1 = self.capture.read()[1]
        buf1 = cv2.flip(self.frame1, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(
            size=(self.frame1.shape[1], self.frame1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
        fps.update()
        
    '''
    def update(self, dt):
        #fps = FPS().start()
        _, self.frame1 = self.capture.read()
        _, self.frame2 = self.capture.read()
        diff = cv2.absdiff(self.frame1, self.frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        erode = cv2.erode(thresh.copy(), None, iterations=10)
        dilated = cv2.dilate(erode, None, iterations=10)
        contours, hier = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
                c = max(contours, key = cv2.contourArea)
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(self.frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(self.frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3) 
        buf1 = cv2.flip(self.frame1, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(
            size=(self.frame1.shape[1], self.frame1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
        '''

    def recordStr(self):
        #cv2.VideoWriter
        return 'recording.....'

    def recordEnd(self):
        return 'recording ended'
    
    def destroy(self):
        cv2.destroyAllWindows()

    def release(self):
        self.capture.release()

class Devices(Screen):

    def __init__(self, **kwargs):
        
        
        super(Devices, self).__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")
        try:
            self.capture = cv2.VideoCapture('http://172.20.10.118:506/video_feed')
            self.devs = Label(text="Detected Devices: " +str(1))
            self.opt = Button(text='RPI')
            self.opt.bind(on_release=self.selectDev)
            layout.add_widget(self.devs)
            layout.add_widget(self.opt)
        except AttributeError:
            raise "No Devices Detected"
            self.devs.text="No Devices Detected"
            
        self.refresh = Button(text="Refresh")
        self.refresh.bind(on_release=self.refreshDevs)
        layout.add_widget(self.refresh)

        self.add_widget(layout)

    def refreshDevs(self, instance):
        self.cam = Devices()
        return self.cam

    def selectDev(self, instance):
        self.parent.current = 'main'

    def read(self):
        return self.capture.read()

    def destroy(self):
        cv2.destroyAllWindows()

    def release(self):
        self.capture.release()

class Account(Screen):

    def __init__(self, **kwargs):
            
        super(Account, self).__init__(**kwargs)
        pass

class MainWindow(Screen):
    
    def __init__(self, **kwargs):
        
        super(MainWindow, self).__init__(**kwargs)

        self.cols = BoxLayout(orientation="vertical", spacing=-800)
        self.box = BoxLayout(orientation="horizontal")

        #self.capture = cv2.VideoCapture('http://10.0.0.249:5000/video_feed')#Devices()
        self.capture = Devices()#cv2.VideoCapture('http://172.20.10.118:5056/video_feed')#172.20.10.118

        self.cam = KivyCamera(capture=self.capture, fps=120)
        self.add_widget(self.cam)

        self.strRec = Button(text='Record', size_hint=(.5,.1))
        self.strRec.bind(on_release=self.strRecord)
        self.box.add_widget(self.strRec)

        self.endRec = Button(text='End Recording', size_hint=(.5,.1))
        self.endRec.bind(on_release=self.endRecord)
        self.box.add_widget(self.endRec)
        
        self.add_widget(self.box)
        
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.output = cv2.VideoWriter('CAPTURE.avi', self.codec, 30, (640, 480))
        self.rec = False
        #self.capture.destroy()
        #self.capture.release()
        

    def menu_Switch(self, instance):
        self.parent.current = 'third'

    def strRecord(self, instance):
        print('recording')
        self.record = True
        #return self.cam.recordStr()

    def endRecord(self, instance):
        print('recording ended')
        #return self.cam.recordEnd
    
        
class NotificationWindow(Screen):

    def __init__(self, **kwargs):
        super(NotificationWindow, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", spacing=-200)

        self.label = Label(text='No records')
        self.layout.add_widget(self.label)
        self.label_one = Label(text='No records')
        self.layout.add_widget(self.label_one)
        self.label_two = Label(text='No records')
        self.layout.add_widget(self.label_two)
        self.label_three = Label(text='No records')
        self.layout.add_widget(self.label_three)
        self.label_four = Label(text='No records')
        self.layout.add_widget(self.label_four)
        
        self.layout2 = BoxLayout(orientation="horizontal")
        
        self.notify = Button(text='Notification', height="50dp", size_hint_y= None)
        self.notify.bind(on_release=self.notify_pressed)
        self.layout2.add_widget(self.notify)

        self.go_back = Button(text='Go Back', height="50dp", size_hint_y= None)
        self.go_back.bind(on_release=self.switch)
        self.layout2.add_widget(self.go_back)

        self.go_back = Button(text='Menu', height="50dp", size_hint_y= None)
        self.go_back.bind(on_release=self.menu_Switch)
        self.layout2.add_widget(self.go_back)
        
        self.add_widget(self.layout)
        self.add_widget(self.layout2)


    def notify_pressed(self, instance):
        key = list(notify.keys())
        value = list(notify.values())
        count = len(notify)
        
        self.label.text = str(key[-1]) + ': '+ str(value[-1])
        self.label_one.text = str(key[count-1]) + ': '+ str(value[count-1])
        self.label_two.text = str(key[count-2]) + ': '+ str(value[count-2])
        self.label_three.text = str(key[count-3]) + ': '+ str(value[count-3])
        self.label_four.text = str(key[count-4]) + ': '+ str(value[count-4])
        
    def switch(self, instance):
        self.parent.current = 'main'

    def menu_Switch(self, instance):
        self.parent.current = 'third'
    
    def menu_pressed(self, instance):
        print('menu pressed')

class MenuWindow(Screen):
    pass
##    def __init__(self, **kwargs):
##            super(NotificationWindow, self).__init__(**kwargs)


class WindowManager(ScreenManager):
    pass

class CamApp(App):
    
    def build(self):
        self.load_kv("my.kv")


if __name__ == '__main__':
    CamApp().run()
