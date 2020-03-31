#!/usr/bin/env python3
# import synthmodule as SM
# import vidmodule as VM
from synthmodule import *
from vidmodule   import *

def convertToRange(oldValue, oldMin, oldMax, newMin, newMax):
    oldRange = (oldMax - oldMin)
    newRange = (newMax - newMin)
    newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
    return newValue

# for fixing openCV y axis
def fixCoord(val, max):
    newVal = max - val
    return newVal

# all variables

minFreq = 225
maxFreq = 1000

minMod = 0
maxMod - 0.0022

rate = 44100 # samples/s

vidWidth = None
vidHeight = None

# dont need min and max gain

with AudioIO(True) as player:
    synth1 = MySynth(minFreq, 0, 0)
    synth2 = MySynth(minFreq, 0, 0)
    synth3 = MySynth(minFreq, 0, 0)
    synth4 = MySynth(minFreq, 0, 0)
    all_synths = [synth1, synth2, synth3, synth4]

    s1 = player.play(sinusoid(synth1.freqStream * Hz) * (synth1.gainStream * 4 * (sinusoid(s1.modStream))))
    s2 = player.play(sinusoid(synth2.freqStream * Hz) * (synth2.gainStream * 4 * (sinusoid(s2.modStream))))
    s3 = player.play(sinusoid(synth3.freqStream * Hz) * (synth3.gainStream * 4 * (sinusoid(s3.modStream))))
    s4 = player.play(sinusoid(synth4.freqStream * Hz) * (synth4.gainStream * 4 * (sinusoid(s4.modStream))))

    all_players = [s1, s2, s3, s4]

    #       BEGIN VIDEO PROCESSING

    detector = getBlobDetect()
    cap = cv2.VideoCapture(0)

    if (cap.isOpened() == False):
        print("error opening file")
    else:
        vidWidth  = int(cap.get(3))
        vidHeight = int(cap.get(4))
        print("width = "  + str(vidWidth))
        print("height = " + str(vidHeight))

    while(cap.isOpened()):
        ret, im = cap.read()
        cv2.imshow("original frame", im)
        cv2.waitKey(1)

        if ret == False:
            print("No image found")

        if ret == True:
            im = processImg(im)
            im_with_keypoints, keypoints = detectFrame(detector, im)

            for synth in all_synths:
                synth.resetModify()

            # trying to figure out how to increment through updating each synth
            # as we iterate through the list of keypoints
            # one option: make array of x and y coordinates of all keypoints
            # then
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

            for synth in all_synths:
                synth.checkModify()

            cv2.imshow("Keypoints", im_with_keypoints)
            cv2.waitKey(1)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    th2.stop()
