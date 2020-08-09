# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from imutils.video import FPS

from kivy.uix.gridlayout import GridLayout 
from kivy.uix.button import Button, Label

from kivy.uix.behaviors import ButtonBehavior

import kivy 
import cv2


notify = []

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

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
            notify.append([x,y,w,h])
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
            cv2.imshow(self.title, self.image)
            if key == ord('q'):
                running = False
                self.freeSpace()
                sys.exit()

class MainWindow(GridLayout):
        def __init__(self, **kwargs):
            
                super(MainWindow, self).__init__(**kwargs)

                self.cols = 1
                
                self.submit = Button(text='submit')
                self.capture = cv2.VideoCapture(0)
                self.add_widget(KivyCamera(capture=self.capture, fps=120))

                self.inside = GridLayout()
                self.inside.cols = 2

                self.notify = Button(text='Notifications', width=10)
                self.notify.bind(on_press=self.notify_pressed)
                self.inside.add_widget(self.notify)

                self.menu = Button(text='Menu', width=10)
                self.inside.add_widget(self.menu)
                self.menu.bind(on_press=self.menu_pressed)


                self.add_widget(self.inside)
                
                '''
                key = cv2.waitKey(20)
                if key == ord('q'):
                    running = False
                    self.freeSpace()
                    sys.exit()
                    print('q')

                if key == ord('m'):
                    self.paused = True
                    cv2.imshow(self.title, self.image)
                    if key == ord('q'):
                        running = False
                        self.freeSpace()
                        sys.exit()
                '''

        def freeSpace(self):
            
            cv2.destroyAllWindows()
            self.capture.release()

        def notify_pressed(self, instance):
            for i in notify:
                print(i)
                print('notify pressed')

        def menu_pressed(self, instance):
            print('menu pressed')
            

class CamApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    CamApp().run()
