#!/usr/bin/env python3

# 255 = white

# Standard imports
import cv2
import numpy as np;

# Read image in grayscale
im = cv2.imread("crowd.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("image", im)
cv2.waitKey(0)

# remove shadows
#   blur to remove noise
frame = cv2.GaussianBlur(im, (3, 3), 0)

cv2.imshow("blurred image", frame)
cv2.waitKey(0)

#   threshold to remove shadows
grayMin = 0
grayMax = 155
mask = cv2.inRange(frame, grayMin, grayMax)
res = cv2.bitwise_and(frame, frame, mask = mask)

cv2.imshow("masked image", res)
cv2.waitKey(0)

res = cv2.dilate(res, None, iterations = 3)
cv2.imshow("dilated image", res)
cv2.waitKey(0)

res = 255-res
cv2.imshow("inverted image", res)
cv2.waitKey(0)

ret,thresh_img = cv2.threshold(res,250,255,cv2.THRESH_BINARY)
cv2.imshow("binary image", thresh_img)
cv2.waitKey(0)

# Detect blobs.
detector = cv2.SimpleBlobDetector_create()
keypoints = detector.detect(thresh_img)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
