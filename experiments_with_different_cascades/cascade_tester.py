import cv2
import glob

"""
A simple script for testing out the effectiveness of a bunch of different
cascades all at once.  the majority of the cascades come from (and are
labelled based on) this link http://alereimondo.no-ip.org/OpenCV/34 and from
SimpleCV (http://simplecv.org/, which seem very similar, albeit slightly
different to the OpenCV ones)
"""


video_src = 0
cam = cv2.VideoCapture(video_src)
cascades =  glob.glob("cascade/*.xml")
current_cascade = 0

print 'Press enter to switch to next cascade'
print 'Press escape to exit'

while True:
    ret, img = cam.read()
    if ret and len(cascades) > 0:
        classifier = cv2.CascadeClassifier(cascades[current_cascade])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = classifier.detectMultiScale(gray, 1.10, 8)
        for x, y, width, height in rects:
            cv2.rectangle(img, (x, y), (x+width, y+height), (255,0,0), 2)
        cv2.imshow(cascades[current_cascade], img)
        key_press = cv2.waitKey(20)
        if key_press == 27:
            print 'closing'
            cv2.destroyAllWindows()
            cam.release()
            break
        elif key_press == 13:
            if current_cascade == len(cascades)-1:
                print 'full cycle done, all methods checked'
            else:
                current_cascade += 1
    else:
        break
            
                              
