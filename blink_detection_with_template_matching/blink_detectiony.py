import cv2
import winsound
from collections import deque

'''
to do:
- try image matching on the section of the eyes detected
'''

'''
This allows basic blink detection using template matching.
'''


video_src = 0
eye_cascade = cv2.CascadeClassifier('eyes.xml')
cam = cv2.VideoCapture(video_src)
previous_eyes_que = deque([])
time_frame = 3
wait_while_loading = 40
comparing_histograms = True
COMP_METHOD = 'cv2.TM_CCOEFF_NORMED'
open_eyes = cv2.imread('open.png',0)
shut_eyes = cv2.imread('blink.png',0)

while True:
  ret, img = cam.read()
  if ret:
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      rects = eye_cascade.detectMultiScale(gray, 1.10, 8)
      if len(rects) == 0:
        #the eyes have not been detected
        print 'no eyes found in camera, searching the whole image'
        search_image = gray
      else:
        #the eyes are currently being detected
        big_width = 0
        big_height = 0
        search_image = None
        for x, y, width, height in rects:
          if(width > big_width and height > big_height):
            big_width = width
            big_height = height
            cv2.rectangle(img, (x, y), (x+width, y+height), (255,0,0), 2)
            search_image = gray[y:y+height, x:x+width]
        #EVENTUALLY - I want to save the search_image here if eyes were
            #successfully found, for use in subsequent iterations (to account
            #for small changes in light over time
      if search_image is not None:
        #then we compare them to detect blinks
        method = eval(COMP_METHOD)
        shut_res = cv2.matchTemplate(search_image,shut_eyes,method)
        min_shut_val, max_shut_val, min_shut_loc, max_shut_loc = \
            cv2.minMaxLoc(shut_res)
        open_res = cv2.matchTemplate(search_image,open_eyes,method)
        min_open_val, max_open_val, min_open_loc, max_open_loc = \
            cv2.minMaxLoc(open_res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
          print min_shut_val, min_open_val
          if min_shut_val < min_open_val:
            blink = True
          else:
            blink = False
        else:
          print max_shut_val, max_open_val
          if max_shut_val > max_open_val:
            blink = True
          else:
            blink = False
        if blink:
          winsound.Beep(2500, 400)
          print 'blink detected'
          print '=='
      cv2.imshow('eyedetect', img)
      key_press = cv2.waitKey(20)
      if key_press == 27:
        #if escape is hit then the program shuts down
        cv2.destroyAllWindows()
        break
  else:
    break



