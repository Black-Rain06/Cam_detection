import cv2
import sys
from flask import Flask, render_template, Response
from webcamvideostream import WebcamVideoStream
import time
import threading

#print(cv2.__version__)
assert(cv2.__version__=='4.3.0')

app = Flask(__name__)

last_epoch = 0


@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        if camera.stopped:
            break
        frame1 = camera.read()
##        gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
##        blur = cv2.GaussianBlur(gray, (5,5), 0)
##
##        ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
##        #        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
##        erode = cv2.erode(thresh, None, iterations=10)
##        dilated = cv2.dilate(erode, None, iterations=10)
##
##        contours, hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
##        
##        for contour in contours:
##            if cv2.contourArea(contour) < 10000 and cv2.contourArea(contour) > 5000:
##                (x,y,w,h) = cv2.boundingRect(contour)
##                cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 3)
        ret, jpeg = cv2.imencode('.jpg',frame1)
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

@app.route('/video_feed')
def video_feed():
    return Response(gen(WebcamVideoStream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
