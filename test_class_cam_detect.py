from class_cam_detect import*


def main():

    cam = doorBellCam('Cam 1: Front Door')
    while cam.paused == True:
        key2 = cv2.waitKey(20)
        if key2 == ord('r'):
            cam.resume()

if __name__ == '__main__':
    while True:
        main()
        if running == False:
            break
