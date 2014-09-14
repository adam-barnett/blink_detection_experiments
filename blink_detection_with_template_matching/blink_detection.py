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
OPENCV_METHODS = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
open_eyes = cv2.imread('open.png',0)
shut_eyes = cv2.imread('blink.png',0)
match_values = {'cv2.TM_CCOEFF':[], 'cv2.TM_CCOEFF_NORMED':[],
                'cv2.TM_CCORR':[],'cv2.TM_CCORR_NORMED':[],
                'cv2.TM_SQDIFF':[], 'cv2.TM_SQDIFF_NORMED':[]}
graph_blinks = []

while True:
  ret, img = cam.read()
  if ret:
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      rects = eye_cascade.detectMultiScale(gray, 1.10, 8)
      if len(rects) == 0:
        #the eyes have not been detected
        print 'no eyes found in camera'
      else:
        #the eyes are currently being detected
        big_width = 0
        big_height = 0
        next_eyes = None
        for x, y, width, height in rects:
          if(width > big_width and height > big_height):
            big_width = width
            big_height = height
            cv2.rectangle(img, (x, y), (x+width, y+height), (255,0,0), 2)
            eye_section = gray[y:y+height, x:x+width]
            next_eyes = eye_section
        if next_eyes is not None:
          #then we compare them to detect blinks
          graph_blinks.append(0)
          for meth in OPENCV_METHODS:
            method = eval(meth)
            res = cv2.matchTemplate(next_eyes,shut_eyes,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
              value = min_val
            else:
              value = max_val
            match_values[meth].append(value)
      cv2.imshow('eyedetect', img)
      key_press = cv2.waitKey(20)
      if key_press == 27:
        for method, values in match_values.iteritems():
          print method
          print values
          print '====='
          print '====='
        print 'blinks recorded', graph_blinks
        #if escape is hit then the program shuts down
        cv2.destroyAllWindows()
        break
      elif key_press == 32:
        if len(graph_blinks) > 0:
          graph_blinks.pop()
          graph_blinks.append(1)
        print 'eyes just shut/opened'



