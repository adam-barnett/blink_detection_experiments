import cv2
import numpy as np

img = cv2.imread('open1.png',0)
#img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
img = cv2.resize(img, (0,0), fx=2.4, fy=2.4)
ret, disp = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)#  THRESH_TRUNC)
cv2.imshow('binary', disp)

circles = cv2.HoughCircles(disp,cv2.cv.CV_HOUGH_GRADIENT,1.2,200,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
#circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
