import cv2
import math



video_src = 0
cam = cv2.VideoCapture(video_src)
eye_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print 'Press space bar to save images of open eyes'
print 'Press enter to save images of shut eyes'
print 'Press escape to exit'

while True:
    ret, img = cam.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = eye_cascade.detectMultiScale(gray, 1.10, 8,
                                    flags=cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)
        face_img = None
        if len(rects) > 0:
            [x, y, width, height] = rects[0]
            cv2.rectangle(img, (x, y), (x+width, y+height), (255,0,0), 2)
            face_img = img[y:y+height, x:x+width]
            eyes_top = int(y + height * 0.294)
            eyes_bottom = int(math.ceil(y + height * 0.515))
            eye_img = img[eyes_top:eyes_bottom, x:x+width]
            cv2.imshow('eyes_found', eye_img)
        cv2.imshow('current_face_detection', img)
        key_press = cv2.waitKey(20)
        if key_press == 32:
            if face_img is not None:
                print 'saving open eyes'
                cv2.imwrite('open.png', eye_img)
            else:
              print 'no face detected'
        elif key_press == 27:
            print 'closing'
            cv2.destroyAllWindows()
            cam.release()
            break
        elif key_press == 13:
            if face_img is not None:
                print 'saving shut eyes'
                cv2.imwrite('blink.png', eye_img)
            else:
                print 'no face detected'
    else:
        break
            
                              
