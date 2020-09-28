

import cv2

from flask import Flask, render_template, Response
from imutils.video import VideoStream


#print(cv2.__version__)
assert(cv2.__version__=='4.3.0')

app = Flask(__name__)

app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        if camera.stopped:
            break
        frame1 = camera.read()
        ret, jpeg = cv2.imencode('.jpg',frame1)
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoStream(src=0).start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
