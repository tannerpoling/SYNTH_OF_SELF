#!/usr/bin/env python3

# 255 = white

# NOTES:
# Given video has black street, white crosswalk lines
# making it much harder to do consistent detection!
# Might want to implement some measures for smoothness
# like having some sort of averaging / fading of where
# centers are rather than instantaneous calculation / change

# Standard imports
import cv2
import numpy as np;

# Some variables for testing
# maybe use argparse for more flexibility?
DEBUG = True


# Read image in grayscale
cap = cv2.VideoCapture("walk1.mp4")

if (cap.isOpened() == False):
    print("error opening file")

# Set up blob detector
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 30
params.maxThreshold = 256

params.filterByArea = True
# params.minArea = 50
params.minArea = 200
params.maxArea = 1500

params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = True

while (cap.isOpened()):
    ret, im = cap.read()

    detector = cv2.SimpleBlobDetector_create(params)

    if ret == True:

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

        # Detect blobs
        # keypoints = detector.detect(im)
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        boxes, weights = hog.detectMultiScale(im, winStride=(8,8) )
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(im, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)


        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        # im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show keypoints
        # cv2.imshow("Keypoints", im_with_keypoints)
        # cv2.waitKey(1)

        cv2.imshow("keypoints", im)

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
