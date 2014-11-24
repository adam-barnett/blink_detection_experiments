import cv2



video_src = 0
cam = cv2.VideoCapture(video_src)
eye_cascade = cv2.CascadeClassifier('eyes.xml')
open_saved = 0
blink_saved = 0

print 'Press space bar to save images of open eyes'
print 'Press enter to save images of shut eyes'
print 'Press escape to exit'

while True:
    ret, img = cam.read()
    if ret:
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      rects = eye_cascade.detectMultiScale(gray, 1.10, 8)
      big_width = 0
      big_height = 0
      eyes_img = None
      for x, y, width, height in rects:
        if(width > big_width and height > big_height):
          big_width = width
          big_height = height
          cv2.rectangle(img, (x, y), (x+width, y+height), (255,0,0), 2)
          eyes_img = img[y:y+height, x:x+width]
      cv2.imshow('current_eye_detection', img)
      key_press = cv2.waitKey(20)
      if key_press == 32:
        if eyes_img is not None:
          print 'saving open eyes image'
          cv2.imwrite('open%d.png' % open_saved, eyes_img)
          open_saved += 1
        else:
          print 'no eyes detected'
      elif key_press == 27:
        print 'closing'
        cv2.destroyAllWindows()
        break
      elif key_press == 13:
        if eyes_img is not None:
          print 'saving shut eyes image'
          cv2.imwrite('blink%d.png' % blink_saved, eyes_img)
          blink_saved += 1
        else:
          print 'no eyes detected'
    else:
        break
            
                              
