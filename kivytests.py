# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from imutils.video import FPS

from kivy.uix.gridlayout import GridLayout 
from kivy.uix.button import Button, Label

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

from datetime import datetime
import kivy 
import cv2


notify = {}
date = datetime.now()

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.notify = []

    def update(self, dt):
        fps = FPS().start()

        _, frame1 = self.capture.read()
        _, frame2 = self.capture.read()
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
            cv2.rectangle(frame2,(x,y),(x+w*2,y+h*2),(0,0,255),2)
            cv2.rectangle(frame2,(x,y),(x+w*2,y+h*2),(0,255,0),2)
            self.notify.append([x,y,w,h])
            notify[str(date)] = str([x,y,w,h])
            #notify.append([x,y,w,h])
            
            #print('Detected Motion')
        
        frame1 = frame2
        fps.update()
            
        buf1 = cv2.flip(frame1, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(
            size=(frame1.shape[1], frame1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture


#### THIS DOES NOT WORK - MAYBE TRY GETTING KIVY INPUT TO HANDLE DISCISSION ####
        key = cv2.waitKey(20)

        if key == ord('q'):
            running = False
            self.freeSpace()
            sys.exit()
            print('q')

        if key == ord('m'):
            self.paused = True
            cv2.imshow(selGrf.title, self.image)
            if key == ord('q'):
                running = False
                self.freeSpace()
                sys.exit()

    def update_Notify(self):
        return self.notify

class MainWindow(Screen):
    
        def __init__(self, **kwargs):
            
                super(MainWindow, self).__init__(**kwargs)

                self.cols = GridLayout()
                self.cols = 1
                
                self.cam = KivyCamera(cv2.VideoCapture(0), fps=120)
                #self.noti = self.cam.update_Notify()
                
                self.inside = GridLayout()
                self.inside.cols = 2

                self.notify = Button(text='Notification', width=10)
                self.notify.bind(on_release=self.notify_pressed)
                self.inside.add_widget(self.notify)

                self.menu = Button(text='Menu', width=10)
                self.menu.bind(on_press=self.menu_pressed)
                self.inside.add_widget(self.menu)


                self.add_widget(self.inside)
                
                
##                key = cv2.waitKey(20)
##                if key == ord('q'):
##                    running = False
##                    self.freeSpace()
##                    sys.exit()
##                    print('q')
##
##                if key == ord('m'):
##                    self.paused = True
##                    cv2.imshow(self.title, self.image)
##                    if key == ord('q'):
##                        running = False
##                        self.freeSpace()
##                        sys.exit()
                

        def freeSpace(self):
            
            cv2.destroyAllWindows()
            self.capture.release()

        def notify_pressed(self, instance):
            print('hi')

        def menu_pressed(self, instance):
            print('menu pressed')
    

class SecondWindow(Screen):

    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        
        self.inside = GridLayout()
        self.inside.cols = 2

        self.notify = Button(text='Notification', width=10)
        self.notify.bind(on_release=self.notify_pressed)
        self.inside.add_widget(self.notify)

        self.menu = Button(text='Menu', width=10)
        self.menu.bind(on_press=self.menu_pressed)
        self.inside.add_widget(self.menu)

        self.label = Label(text='No records')
        self.inside.add_widget(self.label)

        self.add_widget(self.inside)


    def notify_pressed(self, instance):
        for element in notify:
            self.label.text = element + ': ' + notify[element]

    def menu_pressed(self, instance):
        print('menu pressed')


class WindowManager(ScreenManager):
    pass

#kv = Builder.load_file("my.kv")
class CamApp(App):
    
    def build(self):
        self.load_kv("my.kv")

if __name__ == '__main__':
    CamApp().run()
