import kivy

from sys import argv
from os.path import dirname, join
from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer
import cv2
# check what formats are supported for your targeted devices
# for example try h264 video and acc audo for android using an mp4
# container


class VideoPlayerApp(App):

    def build(self):

        return VideoPlayer(source= "http://10.0.0.44:5000/video_feed" , state='play')


if __name__ == '__main__':
    VideoPlayerApp().run()