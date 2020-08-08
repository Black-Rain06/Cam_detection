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

class Grid_LayoutApp(App): 

    # to build the application we have to 
    # return a widget on the build() function. 
    def build(self):

        # adding GridLayouts in App
        # Defining number of coloumn
        # You can use row as well depends on need
        layout = GridLayout(cols = 2)

        # 1st row
        self.capture = cv2.VideoCapture(0)
        layout.add_widget(KivyCamera(capture=self.capture, fps=120))

        layout.add_widget(Button(text ='Notifications'))
  
        # 2nd row 
        layout.add_widget(Button(text ='Menu'))
  
  
        # returning the layout 
        return layout


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=120)
        return self.my_camera

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    Grid_LayoutApp().run()
    CamApp().run()
