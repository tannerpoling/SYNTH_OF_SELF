#!/usr/bin/env python3


# Standard imports
import cv2
import numpy as np;

# Read image
img = cv2.imread("blob.jpg")
cv2.imshow("image", img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("gray", gray)
cv2.waitKey(0)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
print("params made")

# Change thresholds
params.minThreshold = 1
params.maxThreshold = 50

# Filter by Area.
params.filterByArea = True
params.minArea = 10
params.maxArea = 1000000

# # Filter by Circularity
# params.filterByCircularity = True
# params.minCircularity = 0.5

# # Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87

params.filterByColor = True
params.blobColor = 255;

# Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01

# Create a detector with the parameters
# detector = cv2.SimpleBlobDetector(params)
detector = cv2.SimpleBlobDetector_create(params)
print("detector made")


# Detect blobs.
keypoints = detector.detect(gray)
print("keypoints made")

print(keypoints)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
