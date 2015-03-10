import cv2
import numpy as np
import os
import math


"""
an experiment with finding the eyes by looking for the difference between
subsequent images.  It also finds the rotation of the face initially using
a facial haarcascade.
"""

video_src = 0
cam = cv2.VideoCapture(video_src)
prev_image = None
diff_image = None
blinks_saved = 0
frames_saved = []

print 'Press escape to exit'

class box():
    def __init__(self, t, b, l, r):
        self.t = t
        self.b = b
        self.l = l
        self.r = r

    def biggest_edge(self):
        return max(abs(t-b), abs(l-r))

    def xdist(self, box2):
        closestx = min(abs(box2.l - self.l),
                       abs(box2.l - self.r),
                       abs(box2.r - self.l),
                       abs(box2.r - self.r))
        if ((box2.l > self.l and box2.l < self.r) or
            (box2.r > self.l and box2.r < self.r)):
            closestx = 0
        return closestx

    def dist(self, box2):
        closestx = min(abs(box2.l - self.l),
                       abs(box2.l - self.r),
                       abs(box2.r - self.l),
                       abs(box2.r - self.r))
        closesty = min(abs(box2.t - self.t),
                       abs(box2.t - self.b),
                       abs(box2.b - self.t),
                       abs(box2.b - self.b))
        if ((box2.l > self.l and box2.l < self.r) or
            (box2.r > self.l and box2.r < self.r)):
            closestx = 0
        if ((box2.t > self.t and box2.t < self.b) or
            (box2.b > self.t and box2.b < self.b)):
            closesty = 0
        return math.sqrt(math.pow(closestx,2) + math.pow(closesty,2))

    def centre(self):
        return ((self.l+self.r)/2, (self.t+self.b)/2)
        
    
    

def find_eyes(rects, width, height):
    if len(rects) < 2 or len(rects) > 5:
        return None
    for box1 in rects:
        for box2 in rects:
            (x1,y1) = box1.centre()
            (x2,y2) = box2.centre()
            if  abs(x1-x2) > width / 3 and abs(y1-y2) < height / 10:
                if box1.l > box2.r:
                    return [box2, box1]
                else:
                    return [box1, box2]
    return None

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height),
                            flags=cv2.INTER_LINEAR)
    return result

def find_rotation(img):
    eye_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    angles = [0,2,-2,5,-5 ,10,-10, 15, -15, 20, -20, 25, -25, 30, -30, 35,
              -35, 40, -40, 45, -45, 50, -50, 55, -55, 60, -60, 65, -65, 70,
              -70, 75, -75, 80,  -80, 85, -85, 90, -90, 95, -95, 100, -100,
              105, -105, 110, -110]
    biggest_size = 0
    biggest_angle = None
    biggest_face = []
    for angle in angles:
        print 'angle: ', angle
        rot = rotate_image(img, angle)
        rects = eye_cascade.detectMultiScale(rot, 1.10, 8,
                                    flags=cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)
        if len(rects) > 0:
            [x, y, width, height] = rects[0]
            size = width * height
            if size > biggest_size:
                biggest_angle = angle
                biggest_size = size
                biggest_face = rects[0]
    print 'biggest angle found'
    print biggest_angle
    return (biggest_angle, biggest_face)
        
angle = None
rough_face_rect = []  

while True:
    ret, img = cam.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if angle is not None:
            [x, y, width, height] = rough_face_rect
            rot = rotate_image(gray, angle)[y:y + height, x:x + width]
            if prev_image is not None:
                cv2.imshow('k', rot)
                cv2.absdiff(prev_image, rot, diff_image)
                cv2.imshow('huh',diff_image)
                ret, disp = cv2.threshold(diff_image, 10, 255, cv2.THRESH_BINARY)
                kernel = np.ones((5,5),np.uint8)
                erosion = cv2.erode(disp,kernel,iterations = 1)
                dilation = cv2.dilate(erosion,kernel,iterations = 4)
                contours, hierarchy = cv2.findContours(
                    dilation.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                cv2.imshow('difference', diff_image)
                cv2.imshow("threshold", disp)
                cv2.imshow("eroded and dilated", dilation)
                #cv2.drawContours(img, contours, -1, (0,255,0), 3)
                boxes = []
                for contour in contours:
                    t = 10000
                    l = 10000
                    b = 0
                    r = 0
                    for point in contour:
                        [x,y] = point[0]
                        if x > r:
                            r = x
                        if x < l:
                            l = x
                        if y > b:
                            b = y
                        if y < t:
                            t = y
                    boxes.append(box(t,b,l,r))
                    cv2.rectangle(img, (l,t), (r,b), (255,0,0), 2)
                eyes = find_eyes(boxes, rough_face_rect[2], rough_face_rect[3])
                if eyes is not None and len(eyes) == 2:
                    eye1 = rot[eyes[0].t:eyes[0].b, eyes[0].l:eyes[0].r]
                    cv2.imshow('eye1', eye1)
                    eye2 = rot[eyes[1].t:eyes[1].b, eyes[1].l:eyes[1].r]
                    cv2.imshow('eye2', eye2)
                prev_image = rot
            else:
                prev_image = rot
                diff_image = rot.copy()
        else:
            (angle, rough_face_rect) = find_rotation(gray)
        key_press = cv2.waitKey(20)
        if key_press == 27:
            print 'closing'
            cv2.destroyAllWindows()
            cam.release()
            break
    else:
        cam.release()
        break
        
                              
