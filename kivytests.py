# coding:utf-8
import kivy
kivy.require('1.11.1')
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
import imutils
import sys


notify = {'No records':'',}

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.output = cv2.VideoWriter('CAPTURE.avi', self.codec, 30, (640, 480))
        #self.notify
        self.rec = None
    
    def update(self, dt):
        fps = FPS().start()
        self.frame = self.capture.read()[1]
        if self.frame is not None:
            buf1 = cv2.flip(self.frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture
            fps.update()
            if self.rec==True:
                self.output.write(self.frame)
            elif self.rec==False:
                self.output.release()

    def pic(self):
        print('picture taken kivycam')
        return cv2.imshow('capture', self.capture.read()[1])

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
        '''
        try:
            self.capture = cv2.VideoCapture('http://10.0.0.178:5000/video_feed')
            self.devs = Label(text="Detected Devices: " +str(1))
            self.opt = Button(text='RPI')
            self.opt.bind(on_release=self.selectDev)
            layout.add_widget(self.devs)
            layout.add_widget(self.opt)
        except AttributeError:
            raise "No Devices Detected"
            self.devs.text="No Devices Detected"
        '''
        self.capture = cv2.VideoCapture('http://172.16.0.10:5000/video_feed')
        self.devs = Label(text="Detected Devices: " +str(1))
        self.opt = Button(text='RPI')
        self.opt.bind(on_release=self.selectDev)
        layout.add_widget(self.devs)
        layout.add_widget(self.opt)
            
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

    def pic(self):
        print('picture taken devices')
        return cv2.imshow('capture', self.capture.read()[1])

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

        #self.capture = cv2.VideoCapture('http://10.0.0.178:5000/video_feed')
        self.capture = Devices().capture#cv2.VideoCapture('http://172.20.10.118:5056/video_feed')#172.20.10.118

        self.cam = KivyCamera(capture=self.capture, fps=120)
        self.add_widget(self.cam)

        self.noti = Button(text='Alerts', size_hint=(.5,.1))
        self.noti.bind(on_release=self.alerts)
        self.box.add_widget(self.noti)

        self.strRec = Button(text='Record', size_hint=(.5,.1))
        self.strRec.bind(on_release=self.strRecord)
        self.box.add_widget(self.strRec)

        self.pic = Button(text='Capture', size_hint=(.5,.1))
        self.pic.bind(on_release=self.img)
        self.box.add_widget(self.pic)

        self.endRec = Button(text='End Recording', size_hint=(.5,.1))
        self.endRec.bind(on_release=self.endRecord)
        self.box.add_widget(self.endRec)

        self.menu = Button(text='Menu', size_hint=(.5,.1))
        self.menu.bind(on_release=self.dash)
        self.box.add_widget(self.menu)
        
        self.add_widget(self.box)
        
        #self.capture.destroy()
        #self.capture.release()

    def alerts(self, instance):
        self.parent.current = 'second'

    def img(self, instance):
        return self.cam.pic()

    def dash(self, instance):
        print('in menu')
        pass

    def menu_Switch(self, instance):
        self.parent.current = 'third'
    '''
    def record_one_frame(self):
        return self.output.write(self.cam.frame)
    '''
    
    def strRecord(self, instance):
        print('recording')
        self.cam.rec = True
        '''
        self.rec=True
        while self.rec==True:
            output.write(self.cam.frame)
            if self.endRecord:
                output.release()
            break
        '''
        #return self.cam.recordStr()

    def endRecord(self, instance):
        print('recording ended')
        #self.output.release()
        self.cam.rec = False
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
