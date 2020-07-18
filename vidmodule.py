#!/usr/bin/env python3

import cv2
import numpy as np

# TODO:
# - integrate MOG background subtraction
#     take in background at start, assume no objects on screen
#     (include terminal message talking about this)
#     include this in processImg

DEBUG = True


def getBlobDetect():
    # Set up blob detector
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 30
    params.maxThreshold = 256
    params.filterByArea = True
    params.minArea = 1000
    params.maxArea = 10000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = True

    detector = cv2.SimpleBlobDetector_create(params)

    return detector


def processImg(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # remove shadows
    #   blur to remove noise
    frame = cv2.GaussianBlur(im, (3, 3), 0)

    #   threshold to remove shadows
    grayMin = 0
    grayMax = 125
    mask = cv2.inRange(frame, grayMin, grayMax)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    if DEBUG:
        cv2.imshow("masked image", res)
        cv2.waitKey(1)

    res = cv2.dilate(res, None, iterations = 1)
    res = 255-res
    ret,thresh_img = cv2.threshold(res,250,255,cv2.THRESH_BINARY)

    if DEBUG:
        cv2.imshow("binary image", res)
        cv2.waitKey(1)

    return im


def detectFrame(detector, im):
    keypoints = detector.detect(im)
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return im_with_keypoints, keypoints

# get dimensions of openCV video capture
def getVidBounds(cap):
    vidWidth  = int(cap.get(3))
    vidHeight = int(cap.get(4))
    return vidWidth, vidHeight


# if __name__ == "__main__":
#     detector = getBlobDetect()
#
#     # read frames from VideoCapture
#     cap = cv2.VideoCapture("oneperson.mp4")
#
#     if (cap.isOpened() == False):
#         print("error opening file")
#     else:
#         if DEBUG:
#             print("width = "  + str(int(cap.get(3))))
#             print("height = " + str(int(cap.get(4))))
#
#     while (cap.isOpened()):
#         ret, im = cap.read()
#         if ret == True:
#             im = processImg(im)
#             im_with_keypoints, keypoints = detectFrame(detector, im)
#             cv2.imshow("Keypoints", im_with_keypoints)
#             cv2.waitKey(1)
#
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 break
#
#     cap.release()
#     cv2.destroyAllWindows()
