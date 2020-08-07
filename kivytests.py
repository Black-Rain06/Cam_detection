# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.notify = []

    def update(self, dt):
        
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
            cv2.rectangle(frame1,(x,y),(x+w*2,y+h*2),(0,0,255),2)
            cv2.rectangle(frame2,(x,y),(x+w*2,y+h*2),(0,255,0),2)
            self.notify.append([x,y,w,h])
            print(self.notify)
            #print('Detected Motion')
        
        frame1 = frame2
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


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=120)
        return self.my_camera

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
