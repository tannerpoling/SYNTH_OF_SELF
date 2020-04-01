#!/usr/bin/env python3
from audiolazy import *
import time
import threading
import synthIter as SI
import cv2
import numpy as np


if PYTHON2:
  input = raw_input

rate = 44100 # samples/s
# fstart, fend = 16, 20000 # Hz
intensity = 50 # phons
# chirp_duration = 5 # seconds
# total_duration = 9 # seconds
s, Hz = sHz(rate)
freq2dB = phon2dB.iso226(intensity)

maxgain = 402350.59784068936

DEBUG = True


def finalize(zeros_dur):
  print("Finished!")
  for el in zeros(zeros_dur):
    # yield allows you to return a SEQUENCE of values rather than a singular return.
    # used in generator functions: these functions caSynthIteratorn store state data and use it
    # in subsequent calls! pretty cool
    yield el

def dB2magnitude(logpower):
  return 10 ** (logpower / 20)

# freq = 1e3 * Hz * 2

def getBlobDetect():
    # Set up blob detector
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 30
    params.maxThreshold = 256
    params.filterByArea = True
    params.minArea = 200
    params.maxArea = 1500
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

# for fixing openCV y axis
def fixCoord(val, max):
    newVal = max - val
    return newVal

def convertToRange(oldValue, oldMin, oldMax, newMin, newMax):
    oldRange = (oldMax - oldMin)
    newRange = (newMax - newMin)
    newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
    return newValue

#           START


with AudioIO(True) as player:

#           SYNTH SETUP

    print("START SYNTH AT ZERO VOLUME, MIN FREQ. UPDATE VIA OPENCV VALUES")
    print("MAXGAIN = " + str(maxgain))
    minFreq = 225
    maxFreq = 1000
    freqIter = SI.SynthIter(minFreq)
    freqStream = Stream(freqIter)

    maxgain = maxgain / 18

    minFreqGain = dB2magnitude(freq2dB(minFreq)) / maxgain
    maxFreqGain = dB2magnitude(freq2dB(maxFreq)) / maxgain
    gainIter = SI.SynthIter(0)
    gainStream = Stream(gainIter)

    minMod = 0
    maxMod = 0.0022
    modIter = SI.SynthIter(0)
    modStream = Stream(modIter)
    modSine = sinusoid(modStream)

    th2 = player.play(sinusoid(freqStream * Hz) * (gainStream * 4 * (modSine + 1)))


#           BEGIN VIDEO

    detector = getBlobDetect()
    # cap = cv2.VideoCapture("oneperson.mp4")
    cap = cv2.VideoCapture(0)

    if (cap.isOpened() == False):
        print("error opening file")
    else:
        vidWidth  = int(cap.get(3))
        vidHeight = int(cap.get(4))
        print("width = "  + str(vidWidth))
        print("height = " + str(vidHeight))

    while (cap.isOpened()):
        ret, im = cap.read()
        cv2.imshow("original frame", im)
        cv2.waitKey(1)

        if ret == False:
            print("AAAAAAAAAAAa")

        if ret == True:
            im = processImg(im)
            im_with_keypoints, keypoints = detectFrame(detector, im)

            #       UPDATE SYNTH
            # first: map y coordinate of center to frequency
            #        want to go increase in pitch as things move up the frames
            #        in opencv, top of frame = 0, bottom = max value
            # second: adjust gain accordingly
            # third: try amplitude modulation too
            # print("NUM OBJECTS = " + str(len(keypoints)))

            for index in range(len(keypoints)):
                print("X COORD OF OBJECT " + str(index) + ": " + str(keypoints[index].pt[0]))
            print("len of keypoints = " + str(len(keypoints)))
            for keypoint in keypoints:
                x = keypoint.pt[0]
                y = keypoint.pt[1]
                # fix y coordinate and map to frequency
                fixY = fixCoord(y, vidHeight)
                yToFreq = convertToRange(fixY, 0, vidHeight, minFreq, maxFreq)
                xToMod  = convertToRange(x, 0, vidWidth, minMod, maxMod)
                freqIter.changeValue(yToFreq)
                gainIter.changeValue(dB2magnitude(freq2dB(yToFreq)) / maxgain)
                modIter.changeValue(xToMod)

            cv2.imshow("Keypoints", im_with_keypoints)
            cv2.waitKey(1)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    th2.stop()
