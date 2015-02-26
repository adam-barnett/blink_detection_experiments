import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

"""
file for testing out and timing feature matching, much of the code taken from
here: http://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python
(the second answer)

links for when I return to this:
http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
(should all work once I've installed opencv 3.0 (beta) from here:
http://sourceforge.net/projects/opencvlibrary/files/opencv-win/
following these instructions:
http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html

this link also may be helpful:
http://stackoverflow.com/questions/12508934/error-using-knnmatch-with-opencvpython/12517147#12517147

and this one seems like a good example to follow:
http://code.opencv.org/projects/opencv/repository/revisions/master/entry/samples/python2/feature_homography.py

DEFINITELY also check out VLfeat
http://www.vlfeat.org/

"""


def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2])#, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)


video_src = 0
cam = cv2.VideoCapture(video_src)
wait = 20
while True:
    ret, cam_img = cam.read()
    before = time.time()
    if ret and wait == 0:

        blink = cv2.imread('blink.png',0)
        open_eyes = cv2.imread('open.png', cv2.CV_LOAD_IMAGE_COLOR)# queryImage
        cv2.imshow('open', open_eyes)
        cv2.imshow('camera', cam_img)

        img = cam_img

        img_orb = img.copy()
        img_sift = img.copy()
        img_surf = img.copy()

        orb = cv2.ORB(1000, 1.2)
        kp_orb, des_orb = orb.detectAndCompute(img_orb, None)
        cv2.drawKeypoints(img_orb, kp_orb, img_orb)
        cv2.imshow('orb', img_orb)

        sift = cv2.SIFT()
        kp_sift, des_sift = sift.detectAndCompute(img_sift,None)
        cv2.drawKeypoints(img_sift, kp_sift, img_sift)
        cv2.imshow('sift', img_sift)

        surf = cv2.SURF(400)
        kp_surf, des_surf = surf.detectAndCompute(img_surf, None)
        cv2.drawKeypoints(img_surf, kp_surf, img_surf)
        cv2.imshow('surf', img_surf)

##        img1= open_eyes.copy()
##        img2 = img.copy()

##        # Create ORB detector with 1000 keypoints with a scaling pyramid factor
##        # of 1.2
##        orb = cv2.ORB(1000, 1.2)
##
##        # Detect keypoints of original image
##        (kp1,des1) = orb.detectAndCompute(img1, None)
##
##        # Detect keypoints of rotated image
##        (kp2,des2) = orb.detectAndCompute(img2, None)
##
##        # Create matcher
##        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
##
##        # Do matching
##        orb_matches = bf.match(des1,des2)
##
##        img1_2 = open_eyes.copy()
##        img2_2 = img.copy() 
##
##        sift = cv2.SIFT()
##        kp1_2, des1_2 = sift.detectAndCompute(img1_2,None)
##        kp2_2, des2_2 = sift.detectAndCompute(img2_2,None)
##
##        
##        FLANN_INDEX_KDTREE = 0
##        flann_params = dict(algorithm = FLANN_INDEX_KDTREE,trees = 4)    
##        matcher = cv2.FlannBasedMatcher(flann_params, {})
##
##
##        print kp1_2
##        print kp1
##
##        img_orb = img2.copy()
##        img_sift = img2_2.copy()
##        
##        cv2.drawKeypoints(img2, kp2, img_orb)
##        cv2.imshow('orb', img_orb)
##        cv2.drawKeypoints(img2_2, kp2_2, img_sift)
##        cv2.imshow('sift', img_sift)
##
##        cv2.imshow('open', open_eyes)
##        cv2.imshow('camera', img)
        


##        print des1
##        print des1_2
##        print des2
##        print des2_2
##
##        sift_matches = matcher.knnMatch(np.asarray(des1_2,np.float32),
##                                   np.asarray(des2_2,np.float32), 2)
##        print sift_matches
##        print orb_matches
##
##        # Sort the matches based on distance.  Least distance
##        # is better
##        matches = sorted(sift_matches, key=lambda val: val.distance)
##
##        print matches
##
##        

        # Show only the top 10 matches
        #drawMatches(img1, kp1_2, img2, kp2_2, matches[:10])
        key_press = cv2.waitKey()
        if key_press == 27:
            cv2.destroyAllWindows()
            cam.release()
            break
    else:
        wait -= 1
        time.sleep(0.1)

cam.release()
