

import cv2
import netifaces
import sys
import socket

from flask import Flask, render_template, Response
from imutils.video import VideoStream


#print(cv2.__version__)
#assert(cv2.__version__=='4.3.0')


plat = sys.platform

if plat == 'darwin':
    ipaddr = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']
elif plat == 'win32':
    hostn =socket.gethostname()
    ipaddr = socket.gethostbyname(hostn)
else:
    ipaddr == netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']

print(ipaddr)
app = Flask(__name__)

app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip')
def ip():
    return netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']#ipaddr
#socket.getfqdn()

def gen(camera):
    while True:
        frame1 = camera.read()
        #frame2 = camera.read()
        #diff = cv2.absdiff(frame1, frame2)
        #if frame1 is not None:
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (1,1), 0)
        _, thresh = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY)
        erode = cv2.erode(thresh.copy(), None, iterations=10)
        dilated = cv2.dilate(erode, None, iterations=10)
        contours, hier = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
                c = max(contours, key = cv2.contourArea)
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Movement'), (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3) 
        ret, jpeg = cv2.imencode('.jpg',frame1)
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        cv2.waitKey(1)
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoStream(src=0).start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, threaded=True)
