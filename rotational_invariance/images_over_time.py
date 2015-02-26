import cv2
import os

"""
stores images between frames, so that I can see how much the angle
changes over time
"""

video_src = 0
cam = cv2.VideoCapture(video_src)

print 'Press escape to exit'
count = 0

while True:
    ret, img = cam.read()
    if ret:
      cv2.imshow('current_image', img)
      save_loc = os.path.join('rotation_over_time',
                                        'face%d.png'
                                        % count)
      count += 1
      cv2.imwrite(save_loc, img)
      key_press = cv2.waitKey(20)
      if key_press == 27 or count == 200:
        print 'closing'
        cv2.destroyAllWindows()
        break
    else:
        break
                              
cam.release()
