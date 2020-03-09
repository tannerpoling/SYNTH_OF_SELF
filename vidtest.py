#!/usr/bin/env python3

# 255 = white

# Standard imports
import cv2
import numpy as np;

# Read image in grayscale
cap = cv2.VideoCapture("multiple.mp4")

if (cap.isOpened() == False):
    print("error opening file")

# Set up blob detector
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 0
params.maxThreshold = 256

params.filterByArea = True
# params.minArea = 50
params.minArea = 100
params.maxArea = 1250

params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = True

while (cap.isOpened()):
    ret, im = cap.read()

    detector = cv2.SimpleBlobDetector_create(params)

    if ret == True:
        # remove shadows
        #   blur to remove noise
        frame = cv2.GaussianBlur(im, (3, 3), 0)

        #   threshold to remove shadows
        grayMin = 0
        grayMax = 155
        mask = cv2.inRange(frame, grayMin, grayMax)
        res = cv2.bitwise_and(frame, frame, mask = mask)

        # cv2.imshow("masked image", res)
        # cv2.waitKey(1)

        res = cv2.dilate(res, None, iterations = 4)

        res = 255-res

        ret,thresh_img = cv2.threshold(res,250,255,cv2.THRESH_BINARY)
        # cv2.imshow("binary image", thresh_img)
        # cv2.waitKey(1)

        # Detect blobs
        keypoints = detector.detect(im)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(1)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # Print keypoint centers
        for keypoint in keypoints:
            x = keypoint.pt[0]
            y = keypoint.pt[1]
            s = keypoint.size
            print("BLOB FOUND:")
            print("CENTER X = " + str(x))
            print("CENTER Y = " + str(y))
            print("SIZE = " + str(s))
            print("")

    else:
        break

cap.release()

cv2.destroyAllWindows()
