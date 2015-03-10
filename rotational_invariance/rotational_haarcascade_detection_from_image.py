import cv2
import math
import os


"""
finding the rotation at which a face can be found in a specific image.
"""


def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, (width, height),
                            flags=cv2.INTER_LINEAR)
    return result

video_src = 0
eye_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
save_count = 0
current_angle = 0
face_image = cv2.imread('face.png', 0)
angles = [0,2,5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
          80, 85, 90, 95, 100, 105, 110, 115, 0, 2, -5, -10, -15, -20, -25,
          -30, -35, -40, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90,
          -95, -100, -105, -110, -115]

connected_section = False
longest_section = []
current_section = []

for angle in angles:
    rot = rotate_image(face_image, angle)
    rects = eye_cascade.detectMultiScale(rot,1.10, 8,
                            flags=cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)
    if len(rects) > 0:
        [x, y, width, height] = rects[0]
        cv2.rectangle(rot, (x, y), (x+width, y+height), (255,0,0), 2)
##        cv2.imshow(str(angle), rot)
##        save = str(angle) + ".png"
##        cv2.imwrite(save, rot)
        current_section.append(angle)
    else:
        if len(current_section) > len(longest_section):
            longest_section = current_section
        current_section = []
if len(longest_section) != 0:
    angle = int(sum(longest_section)/len(longest_section))
    rot = rotate_image(face_image, angle)
    [[x, y, width, height]] = eye_cascade.detectMultiScale(rot,1.10, 8,
                            flags=cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)
    cv2.rectangle(rot, (x, y), (x+width, y+height), (255,0,0), 2)
    face_img = rot[y:y+height, x:x+width]
    eyes_top = int(y + height * 0.294)
    eyes_bottom = int(math.ceil(y + height * 0.515))
    eye_img = rot[eyes_top:eyes_bottom, x:x+width]
    cv2.imshow('eyes_found', eye_img)
    cv2.imshow('face found here', rot)
    print 'best face found at angle: ', angle
else:
    cv2.imshow('no face found', face_image)
key_press = cv2.waitKey(0)
cv2.destroyAllWindows()
    
