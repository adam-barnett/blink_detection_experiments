import cv2
import math

"""
Experiments with resizing the image from the camera based on the distance
between two eye templates matched in the previous frame, so that the matching
becomes scale invariant.
Note. the two eye files left.png and right.png need to be captured recently
and original distance needs to be manually set as the distance between them
"""



def resize(image, scale, interpol = cv2.INTER_AREA):
    if scale == 1.0:
        return image
    new_dim = (int(image.shape[1]*scale), int(image.shape[0]*scale))
    resized = cv2.resize(image, new_dim, interpolation = interpol)
    return resized

class resize_rect():
    def __init__(self, loc, shape, scale):
        self.left_top = (int((loc[0] - shape[1])*scale),
                         int((loc[1] - shape[0])*scale))
        self.right_bot = (int((loc[0] + shape[1]*2)*scale),
                          int((loc[1] + shape[0]*2)*scale))
        self.l = self.left_top[0]
        self.t = self.left_top[1]
        self.r = self.right_bot[0]
        self.b = self.right_bot[1]
        


video_src = 0
cam = cv2.VideoCapture(video_src)
l_eye = cv2.imread('left.png',1)
r_eye = cv2.imread('right.png',1)
scale = 1.0
original_distance = 40
prev_distance = original_distance
COMP_METHOD = 'cv2.TM_CCOEFF_NORMED'
left_rect = None
right_rect = None

while True:
    ret, img = cam.read()
    if ret:
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        scaled_img = resize(img, scale)
        method = eval(COMP_METHOD)
        if left_rect is not None and right_rect is not None:
##            cv2.rectangle(scaled_img, left_rect.left_top, left_rect.right_bot,
##                          (255,0,0), 1)
            left_search = scaled_img[left_rect.t:left_rect.b,
                                     left_rect.l:left_rect.r]
##            cv2.rectangle(scaled_img, right_rect.left_top, right_rect.right_bot,
##                          (0,255,0), 1)
            right_search = scaled_img[right_rect.t:right_rect.b,
                                      right_rect.l:right_rect.r]
            cv2.imshow('left', left_search)
            cv2.imshow('right', right_search)
        else:
            left_search = scaled_img
            right_search = scaled_img
        left_found = cv2.matchTemplate(left_search,l_eye,method)
        _, max_l_val, _, max_l_loc = cv2.minMaxLoc(left_found)
        right_found = cv2.matchTemplate(right_search,r_eye,method)
        _, max_r_val, _, max_r_loc = cv2.minMaxLoc(right_found)
        face_img = None
        if max_l_val > 0.65 and max_r_val > 0.65:
            if left_search.shape != scaled_img.shape:
                max_l_loc = (max_l_loc[0] + left_rect.l,
                             max_l_loc[1] + left_rect.t)
            if right_search.shape != scaled_img.shape:
                max_r_loc = (max_r_loc[0] + right_rect.l,
                             max_r_loc[1] + right_rect.t)
            cv2.rectangle(scaled_img, max_l_loc, (max_l_loc[0] + l_eye.shape[1],
                                           max_l_loc[1] + l_eye.shape[0]),
                                          (255,0,0), 2)
            cv2.rectangle(scaled_img, max_r_loc, (max_r_loc[0] + r_eye.shape[1],
                                           max_r_loc[1] + r_eye.shape[0]),
                                          (0,255,0), 2)
            dist = max_r_loc[0] - (max_l_loc[0] + l_eye.shape[1])
            left_y_centre = max_l_loc[1] + (l_eye.shape[0] / 2)
            if(dist != original_distance and
               abs(dist - prev_distance) > 3 and
               (left_y_centre > max_r_loc[1] and
                 left_y_centre < max_r_loc[1] + r_eye.shape[0])):
                    new_scale = ((float(original_distance)/dist) + 3.0)/4
                    prev_distance = dist
                    left_rect = resize_rect(max_l_loc, l_eye.shape,
                                            new_scale/scale)
                    right_rect = resize_rect(max_r_loc, r_eye.shape,
                                             new_scale/scale)
                    scale = new_scale
            elif (left_y_centre > max_r_loc[1] and
                 left_y_centre < max_r_loc[1] + r_eye.shape[0]):
                left_rect = resize_rect(max_l_loc, l_eye.shape,1.0)
                right_rect = resize_rect(max_r_loc, r_eye.shape,1.0)
        if left_rect is not None and right_rect is not None:
            cv2.rectangle(scaled_img, left_rect.left_top, left_rect.right_bot,
                          (255,0,0), 1)
            cv2.rectangle(scaled_img, right_rect.left_top, right_rect.right_bot,
                          (0,255,0), 1)
        cv2.imshow('current_eye_detection', scaled_img)
        key_press = cv2.waitKey(20)
        if key_press == 27:
            print 'closing'
            cv2.destroyAllWindows()
            cam.release()
            break
    else:
        break
        cam.release()
            
                              
