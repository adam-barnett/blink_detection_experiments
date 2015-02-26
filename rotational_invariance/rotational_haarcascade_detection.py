import cv2
import math
import os


"""
Attempting to capture the face for different rotations using haarcascades.
The concept seems to work okay, but the haarcascade is far too slow which
means it fails after a while.
"""


def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height),
                            flags=cv2.INTER_LINEAR)
    return result

video_src = 0
cam = cv2.VideoCapture(video_src)
eye_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
save_count = 0
current_angle = 0
angles = [0,2,-2,5,-5,10,-10]
modifiers_used = []

while True:
    ret, img = cam.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for angle_mod in angles:
            angle_test = current_angle + angle_mod
            gray_rot = rotate_image(gray, angle_test)
            rects = eye_cascade.detectMultiScale(gray_rot,1.10, 8,
                                    flags=cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)
            if len(rects) > 0:
                modifiers_used.append(angle_mod)
                current_angle = angle_test
                print 'face found at angle', current_angle
                break
        if len(rects) > 0:
            [x, y, width, height] = rects[0]
            cv2.rectangle(gray_rot, (x, y), (x+width, y+height), (255,0,0), 2)
            face_img = gray_rot[y:y+height, x:x+width]
            eyes_top = int(y + height * 0.294)
            eyes_bottom = int(math.ceil(y + height * 0.515))
            eye_img = gray_rot[eyes_top:eyes_bottom, x:x+width]
            cv2.imshow('eyes_found', eye_img)
            save_loc = os.path.join('eyes_from_rotations',
                                        'eyes%d.png'
                                        % save_count)
            save_count += 1
            cv2.imwrite(save_loc, eye_img)
            cv2.imshow('current_face_detection', gray_rot)
        else:
            cv2.imshow('current_face_detection', gray)
        key_press = cv2.waitKey(20)
        if key_press == 27:
            print 'closing'
            cv2.destroyAllWindows()
            cam.release()
            break

    else:
        break

print 'angle modifications:'
print modifiers_used
                            
