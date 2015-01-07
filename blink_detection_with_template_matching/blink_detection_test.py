import cv2
import winsound
from collections import deque
import os


'''
This is a test of basic blink detection using template matching.
The images of blinking eyes which it captures are saved to the folder
captured_blinks.
'''


video_src = 0
eye_cascade = cv2.CascadeClassifier('eyes.xml')
cam = cv2.VideoCapture(video_src)
COMP_METHOD = 'cv2.TM_CCOEFF_NORMED'
open_eyes = cv2.imread('open.png',0)
shut_eyes = cv2.imread('blink.png',0)
shut_shape = shut_eyes.shape
open_shape = open_eyes.shape
blinks_saved = 0

while True:
  ret, img = cam.read()
  if ret:
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      rects = eye_cascade.detectMultiScale(gray, 1.10, 8)
      if len(rects) == 0:
        #the eyes have not been detected
        print 'no eyes found in camera, searching the whole image'
        search_image = gray
        pos = None
      else:
        #the eyes are currently being detected
        big_width = 0
        big_height = 0
        search_image = None
        pos = None
        for x, y, width, height in rects:
          if(width > big_width and height > big_height):
            big_width = width
            big_height = height
            pos = (x,y)
        if big_width != 0 and big_height != 0:
          if big_width < shut_shape[1] or big_width < open_shape[1]:
            big_width = max(shut_shape[1], open_shape[1])
          if big_height < shut_shape[0] or big_height < open_shape[0]:
            big_height = max(shut_shape[0], open_shape[0])
          cv2.rectangle(img, (pos[0], pos[1]),
                        (pos[0]+big_width, pos[1]+big_height), (255,0,0), 2)
          search_image = gray[pos[1]:pos[1]+big_height,
                              pos[0]:pos[0]+big_width]
          print search_image.shape
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
          if min_shut_val < min_open_val:
            blink = True
            blink_pos = min_shut_loc
          else:
            blink = False
        else:
          print max_shut_val, max_open_val
          if max_shut_val > max_open_val:
            blink = True
            blink_pos = max_shut_loc
          else:
            blink = False
        if blink:
          if pos is not None:
            blink_pos = (blink_pos[0] + pos[0], blink_pos[1] + pos[1])
          blink_img = img[blink_pos[1]:blink_pos[1]+shut_shape[0],
                          blink_pos[0]:blink_pos[0]+shut_shape[1]]
          blink_bottom_right = (blink_pos[0] + shut_shape[1],
                          blink_pos[1] + shut_shape[0])
          cv2.rectangle(img, blink_pos, blink_bottom_right, 255, 2)
          blink_save_loc = os.path.join('captured_blinks', 'blink_number%d.png' % blinks_saved)
          #EVENTUALLY - I want to save the blink_img here if eyes were
            #successfully found, for use in subsequent iterations (to account
            #for small changes in light over time)
          cv2.imwrite(blink_save_loc, blink_img)
          cv2.imshow('blinkdetect%d' %blinks_saved, blink_img)
          blinks_saved += 1
          winsound.Beep(2500, 200)
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



