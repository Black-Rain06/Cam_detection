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


notify = {'No records':'',}

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        #self.notify

    def update(self, dt):
        fps = FPS().start()
        _, self.frame1 = self.capture.read()
        _, self.frame2 = self.capture.read()
        diff = cv2.absdiff(self.frame1, self.frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        erode = cv2.erode(thresh.copy(), None, iterations=10)
        dilated = cv2.dilate(erode, None, iterations=10)
        contours, hier = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)
            #self.notify.append([x,y,w,h])
            rect = cv2.rectangle(self.frame2,(x,y),(x+w*2,y+h*2),(0,0,255),4)
            notify[str(datetime.now())] = str([x,y,w,h])
        self.frame1 = self.frame2
        fps.update()
            
        buf1 = cv2.flip(self.frame1, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(
            size=(self.frame1.shape[1], self.frame1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
    

    def destroy(self):
        cv2.destroyAllWindows()

    def release(self):
        self.capture.release()

class Devices(Screen):

    def __init__(self, **kwargs):
        
        
        super(Devices, self).__init__(**kwargs)
        self.capture = doorBellApp()
        self.cam = self.capture.available_dev()
        self.num = len(self.cam)
        layout = BoxLayout(orientation="vertical")
        self.devs = Label(text="Detected Devices: " +str(self.num))
        layout.add_widget(self.devs)
        if len(self.capture.inname)>0:
            self.opt = Button(text=self.capture.inname)
            self.opt.bind(on_release=self.selectDev)
            layout.add_widget(self.opt)
        elif len(self.capture.inname) == 0:#and len(self.capture.exname) == 0:
            for i in self.capture.exname:
                self.opt = Button(text=i)
                self.opt.bind(on_release=self.selectDev)
                layout.add_widget(self.opt)
        else:
            layout.add_widget(Label(text="No Devices Detected"))
            
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

        self.cols = BoxLayout(orientation="horizontal", spacing=-800)

        self.capture = cv2.VideoCapture('http://10.0.0.249:5000/video_feed')#Devices()
        
        self.cam = KivyCamera(capture=self.capture, fps=120)
        self.add_widget(self.cam)
        #self.capture.destroy()
        #self.capture.release()

    def menu_Switch(self, instance):
        self.parent.current = 'third'
    
        
class NotificationWindow(Screen):

    def __init__(self, **kwargs):
        super(NotificationWindow, self).__init__(**kwargs)
        
##        self.inside = GridLayout()
##        self.inside.cols = 1
##
##        self.notify = Button(id='how', text='Notification', height="50dp", size_hint_y= None)
##        self.notify.bind(on_release=self.notify_pressed)
##        self.inside.add_widget(self.notify)
        
        '''
        self.label = Label(text='No records')
        self.inside.add_widget(self.label)
        self.label_one = Label(text='No records')
        self.inside.add_widget(self.label_one)
        self.label_two = Label(text='No records')
        self.inside.add_widget(self.label_two)
        self.label_three = Label(text='No records')
        self.inside.add_widget(self.label_three)
        self.label_four = Label(text='No records')
        self.inside.add_widget(self.label_four)
        
        self.label_five = Label(text='No records')
        self.inside.add_widget(self.label_five)
        self.label_six = Label(text='No records')
        self.inside.add_widget(self.label_six)
        self.label_seven = Label(text='No records')
        self.inside.add_widget(self.label_seven)
        self.label_eight = Label(text='No records')
        self.inside.add_widget(self.label_eight)
        self.label_nine = Label(text='No records')
        self.inside.add_widget(self.label_nine)
        
        self.label_ten = Label(text='No records')
        self.inside.add_widget(self.label_ten)
        self.label_eleven = Label(text='No records')
        self.inside.add_widget(self.label_eleven)
        self.label_twelve = Label(text='No records')
        self.inside.add_widget(self.label_twelve)
        self.label_thirteen = Label(text='No records')
        self.inside.add_widget(self.label_thirteen)
        self.label_fifteen = Label(text='No records')
        self.inside.add_widget(self.label_fifteen)
        
        self.label_sixteen = Label(text='No records')
        self.inside.add_widget(self.label_sixteen)
        self.label_seventeen = Label(text='No records')
        self.inside.add_widget(self.label_seventeen)
        self.label_eighteen = Label(text='No records')
        self.inside.add_widget(self.label_eighteen)
        self.label_nineteen = Label(text='No records')
        self.inside.add_widget(self.label_nineteen)
        
        self.go_back = Button(text='Go Back')
        self.go_back.bind(on_release=self.switch)
        self.inside.add_widget(self.go_back)
        self.go_back = Button(text='Menu')
        self.go_back.bind(on_release=self.menu_Switch)
        self.inside.add_widget(self.go_back)
        '''

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
        '''
        self.label_five.text = str(key[count-5]) + ': '+ str(value[count-5])
        self.label_six.text = str(key[count-6]) + ': '+ str(value[count-6])
        self.label_seven.text = str(key[count-7]) + ': '+ str(value[count-7])
        self.label_eight.text = str(key[count-8]) + ': '+ str(value[count-8])
        self.label_nine.text = str(key[count-9]) + ': '+ str(value[count-9])
        
        self.label_ten.text = str(key[count-10]) + ': '+ str(value[count-10])
        self.label_eleven.text = str(key[count-11]) + ': '+ str(value[count-11])
        self.label_twelve.text = str(key[count-12]) + ': '+ str(value[count-12])
        self.label_thirteen.text = str(key[count-13]) + ': '+ str(value[count-13])
        self.label_fifteen.text = str(key[count-14]) + ': '+ str(value[count-14])
        
        self.label_sixteen.text = str(key[count-16]) + ': '+ str(value[count-16])
        self.label_seventeen.text = str(key[count-17]) + ': '+ str(value[count-17])
        self.label_eighteen.text = str(key[count-18]) + ': '+ str(value[count-18])
        self.label_nineteen.text = str(key[count-19]) + ': '+ str(value[count-19])
        '''
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
