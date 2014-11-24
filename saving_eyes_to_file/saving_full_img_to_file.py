import cv2


video_src = 0
cam = cv2.VideoCapture(video_src)
saved = 0

print 'Press space bar to save image displayed'
print 'Press escape to exit'

while True:
    ret, img = cam.read()
    if ret:
      cv2.imshow('current_image', img)
      key_press = cv2.waitKey(20)
      if key_press == 32:
        print 'saving image'
        cv2.imwrite('image%d.png' % saved, img)
        saved += 1
      elif key_press == 27:
        print 'closing'
        cv2.destroyAllWindows()
        break
    else:
        break
                              
