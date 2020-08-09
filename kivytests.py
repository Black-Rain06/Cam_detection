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
from kivy.uix.widget import Widget


from datetime import datetime
import kivy 
import cv2


notify = {'No records':'',}

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
            date = datetime.now()
            notify[str(date)] = str([x,y,w,h])
        frame1 = frame2
        fps.update()
            
        buf1 = cv2.flip(frame1, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(
            size=(frame1.shape[1], frame1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture

    def update_Notify(self):
        return self.notify

    def freeSpace(self):
        cv2.destroyAllWindows()
        self.capture.release()

class MainWindow(Screen):
    
        def __init__(self, **kwargs):
            
                super(MainWindow, self).__init__(**kwargs)

                self.cols = GridLayout(cols = 1)

                self.cam = cv2.VideoCapture(0)
                self.cam = KivyCamera(capture=self.cam, fps=120)
                self.add_widget(self.cam)
                self.noti = self.cam.update_Notify()

        def menu_Switch(self, instance):
            self.parent.current = 'third'  
    

class NotificationWindow(Screen):

    def __init__(self, **kwargs):
        super(NotificationWindow, self).__init__(**kwargs)
        
        self.inside = GridLayout()
        self.inside.cols = 1

        self.notify = Button(id='how', text='Notification', height="50dp", size_hint_y= None)
        self.notify.bind(on_release=self.notify_pressed)
        self.inside.add_widget(self.notify) 
        
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

        self.add_widget(self.inside)


    def notify_pressed(self, instance):
        key = list(notify.keys())
        value = list(notify.values())
        count = len(notify)
        
        self.label.text = str(key[-1]) + ': '+ str(value[-1])
        self.label_one.text = str(key[count-1]) + ': '+ str(value[count-1])
        self.label_two.text = str(key[count-2]) + ': '+ str(value[count-2])
        self.label_three.text = str(key[count-3]) + ': '+ str(value[count-3])
        self.label_four.text = str(key[count-4]) + ': '+ str(value[count-4])
        
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
