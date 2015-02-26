from sift_matching import compare
import cv2
import time
import winsound

"""
Checking how effective feature matching is in real time and whether it's
fast enough
"""



video_src = 0
cam = cv2.VideoCapture(video_src)
blink_img = cv2.imread('blink.png', 0)
open_img = cv2.imread('open.png', 0)

print 'press space bar when you are blinking'
blink_vals = [0,0]
open_vals = [0,0]
all_vals_blink = []
all_vals_open = []
iterations = 0
total_time = 0

while True:
    ret, img = cam.read()
    before = time.time()
    if ret:
        cv2.imshow('current_image', img)
        open_comp = compare(img, open_img)
        blink_comp = compare(img, blink_img)
        key_press = cv2.waitKey(20)
        if blink_comp > open_comp:
            winsound.Beep(2500, 50)
            print 'YOU DUN BLUNK!'
        else:
            print 'NO BLUNK HERE'
        if key_press == 27:
            print 'closing'
            cv2.destroyAllWindows()
            cam.release()
            break
        if key_press == 32:
            blink_vals[0] = blink_vals[0] + blink_comp
            blink_vals[1] = blink_vals[1] + open_comp
        else:
            open_vals[0] = open_vals[0] + blink_comp
            open_vals[1] = open_vals[1] + open_comp
        iterations += 1
        total_time = total_time + time.time() - before
        all_vals_blink.append(blink_comp)
        all_vals_open.append(open_comp)
        before = time.time()
    else:
        break

print 'blink values ',
print blink_vals
print 'open_values ',
print open_vals
print 'iterations ' + str(iterations)
print 'avg time per iteration = ' + str(total_time/float(iterations))
print all_vals_blink
print all_vals_open
                       
