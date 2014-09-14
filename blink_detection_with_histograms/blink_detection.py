import cv2
import winsound
from collections import deque

'''
This allows basic blink detection using histogram comparison.  To compare the
different histogram comparisong methods set comparing_histograms to True
(and press space bar to mark each blink).
'''


video_src = 0
eye_cascade = cv2.CascadeClassifier('eyes.xml')
cam = cv2.VideoCapture(video_src)
show_detected_eyes = True
hist_previous_eyes_que = deque([])
time_frame = 3
wait_while_loading = 40
comparing_histograms = True
OPENCV_METHODS = (
    ("Correlation", cv2.cv.CV_COMP_CORREL),
    ("Chi-Squared", cv2.cv.CV_COMP_CHISQR),
    ("Intersection", cv2.cv.CV_COMP_INTERSECT),
    ("Hellinger", cv2.cv.CV_COMP_BHATTACHARYYA))
graph_histograms = {
    "Correlation": [],
    "Chi-Squared": [],
    "Intersection": [],
    "Hellinger": [],}
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
            if show_detected_eyes:
              cv2.imshow('eye', eye_section)
        if next_eyes is not None:
          #then we compare them to detect blinks
          hist_new_eyes = cv2.calcHist([next_eyes],[0],None,[256],[0,256])
          hist_previous_eyes = None
          hist_previous_eyes_que.append(hist_new_eyes)
          if len(hist_previous_eyes_que) > time_frame:
            hist_previous_eyes = hist_previous_eyes_que.popleft()
            if wait_while_loading > 0:
              wait_while_loading -= 1
          if hist_previous_eyes is not None and wait_while_loading == 0:
            distance = cv2.compareHist(hist_new_eyes, hist_previous_eyes,
                                       cv2.cv.CV_COMP_CHISQR)
            graph_blinks.append(0)
            if distance > 1000:
              print 'blink detected'
              hist_previous_eyes_que.clear()
            if comparing_histograms:
              for method_name, method in OPENCV_METHODS:
                distance = cv2.compareHist(hist_new_eyes, hist_previous_eyes,
                                       method)
                #print 'distance found for ', method_name, 'is', distance
                graph_histograms[method_name].append(distance)
              print '===='
      cv2.imshow('eyedetect', img)
      key_press = cv2.waitKey(20)
      if key_press == 27:
        #if escape is hit then the program shuts down
        if comparing_histograms:
          for method, numbers in graph_histograms.iteritems():
            print method
            print numbers
            print '=='
          print 'rough blink locations'
          print graph_blinks
        cv2.destroyAllWindows()
        break
      elif key_press == 32:
        if len(graph_blinks) > 0:
          graph_blinks.pop()
          graph_blinks.append(1)
        print 'eyes just shut/opened'



