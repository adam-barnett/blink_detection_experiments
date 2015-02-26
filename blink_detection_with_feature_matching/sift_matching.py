import cv2
import numpy as np
import itertools
import sys

"""
matching the keypoints found with SURF to a given image
"""

def findKeyPoints(img, template, distance=200):
    name = "SURF"
    detector = cv2.FeatureDetector_create(name)
    descriptor = cv2.DescriptorExtractor_create(name)

    skp = detector.detect(img)
    skp, sd = descriptor.compute(img, skp)

    tkp = detector.detect(template)
    tkp, td = descriptor.compute(template, tkp)

    flann_params = dict(algorithm=1, trees=8)
    flann = cv2.flann_Index(sd, flann_params)
    idx, dist = flann.knnSearch(td, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    skp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            skp_final.append(skp[i])

    flann = cv2.flann_Index(td, flann_params)
    idx, dist = flann.knnSearch(sd, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    tkp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            tkp_final.append(tkp[i])

    return skp_final, tkp_final

def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    print h1, w2, w1, h2
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    print template.shape
    print img.shape
    print newimg.shape
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in range(num):
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
        cv2.line(newimg, pt_a, pt_b, (255, 0, 0))
    return newimg


def compare(big_img, small_img):
    dist = 30
    num = 200
    skp, tkp = findKeyPoints(big_img, small_img, dist)
    return len(tkp)


def match():
    img = cv2.imread('face.png')
    temp = cv2.imread('open.png')
    #temp = cv2.resize(temp, (0,0), fx=2, fy=2)
    cv2.imshow('face', img)
    cv2.imshow('eyes', temp)
    dist = 30
    num = 200
    skp, tkp = findKeyPoints(img, temp, dist)
    print len(tkp)
    print len(skp)
    newimg = drawKeyPoints(img, temp, skp, tkp, num)
    cv2.imshow("image", newimg)
    cv2.imwrite('bam.png', newimg)
    key_press = cv2.waitKey()
    if key_press == 27:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    match()
