#!/usr/bin/env python3
# import synthmodule as SM
# import vidmodule as VM
from synthmodule    import *
from vidmodule      import *
from harmonymodule  import *
from plotmodule     import *

# TODO:
# - integrate harmony detection -> draw something on screen
# - improve background subtraction / foreground mask


def convertToRange(oldValue, oldMin, oldMax, newMin, newMax):
    oldRange = (oldMax - oldMin)
    newRange = (newMax - newMin)
    newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
    return newValue

# for fixing openCV y axis
def fixCoord(val, max):
    newVal = max - val
    return newVal

# get current state of array of synths
def getStates(synths):
    allFreq = [0] * len(synths)
    allGain = [0] * len(synths)
    allMod = [0] * len(synths)
    for i in range(len(synths)):
        allFreq[i], allGain[i], allMod[i] = synths[i].peekState()
    return allFreq, allGain, allFreq

def getFreqs(synths):
    allFreq = [0] * len(synths)
    for i in range(len(synths)):
        allFreq[i] = synths[i].peekFreq()
    return sorted(allFreq)

def updateSynths(centroids):
    # TODO: use an ordered set of cetroids to achieve ordering of synths!!
    #       test this functionality with simple print statements
    for index in range(len(centroids)): # loop thru detected objects, update synths
        if index > (len(all_synths) - 1):
            pass
        else:
            x = int(centroids[index][0])
            y = int(centroids[index][1])

            fixY = fixCoord(y, vidHeight)

            if heatmap_en:
                heatmapData[x][fixY] += 1

            # update frequency and modulation
            global test_count, test_modval

            yToFreq = convertToRange(fixY, 0, vidHeight, minFreq, maxFreq)
            xToMod  = convertToRange(x, 0, vidWidth, minMod, maxMod)
            if test_count % test_modval == 0:
                all_synths[index].changeFreq(yToFreq / 2)
                all_synths[index].changeMod(xToMod / 2)
            else:
                all_synths[index].changeFreq(yToFreq)
                all_synths[index].changeMod(xToMod)

            test_count = test_count + 1

    # check harmony and update gain of harmonious synths


    for synth in all_synths:
        synth.checkModify() # makes sure that each synth is actively being used
                            # turns off volume otherwise


# all variables

minFreq = 225
maxFreq = 1000

minMod = 0
maxMod = 0.0022
# maxMod = 0 # set to zero to disable modulation. maybe use true/false variable?

# new: experimenting with variable sample rate
rate_min = 22000
rate_max = 44100
rate = 44100 # samples/s
test_count = 0
test_modval = 2

s, Hz = sHz(rate)

vidWidth = None
vidHeight = None
heatmapData = None

extraGain = 20

bgSubtract = True

heatmap_en = False
DEBUG = True

vidSource = 0 # 0 -> webcam, "/dev/video2" -> usb webcam

with AudioIO(True) as player:

    #       SET UP ALL SYNTHS

    synth1 = MySynth(minFreq, 0, 0)
    synth2 = MySynth(minFreq, 0, 0)
    synth3 = MySynth(minFreq, 0, 0)
    synth4 = MySynth(minFreq, 0, 0)
    all_synths = [synth1, synth2, synth3, synth4]

    s1 = player.play(sinusoid(synth1.freqStream * Hz) * extraGain * (synth1.gainStream * 4 * (sinusoid(synth1.modStream) + 1)))
    s2 = player.play(sinusoid(synth2.freqStream * Hz) * extraGain * (synth2.gainStream * 4 * (sinusoid(synth2.modStream) + 1)))
    s3 = player.play(sinusoid(synth3.freqStream * Hz) * extraGain * (synth3.gainStream * 4 * (sinusoid(synth3.modStream) + 1)))
    s4 = player.play(sinusoid(synth4.freqStream * Hz) * extraGain * (synth4.gainStream * 4 * (sinusoid(synth4.modStream) + 1)))

    all_players = [s1, s2, s3, s4]

    #       BEGIN VIDEO PROCESSING

    cap = cv2.VideoCapture(vidSource)

    if (cap.isOpened() == False):
        print("error opening file / connecting to webcam!")
    else:
        vidWidth  = int(cap.get(3))
        vidHeight = int(cap.get(4))
        print("video width = "  + str(vidWidth))
        print("video height = " + str(vidHeight))

        if heatmap_en:
            heatmapData = np.ones(shape=(vidWidth,vidHeight))
            print("heatmap shape: " + str(heatmapData.shape))


    # SUBTRACT BACKGROUND (for MOG subtraction method)

    print("Subtracting background, remove all objects from frame!")
    time.sleep(2)
    backSub = cv2.createBackgroundSubtractorMOG2()
    backSub.setDetectShadows(False)
    # backSub.setHistory(1)
    ret, im = cap.read()
    fgMask = backSub.apply(im, None, 1.0)
    time.sleep(2)



    # START SYNTH OF SELF

    while(cap.isOpened()):

        ret, im = cap.read()
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        cv2.imshow("original frame", im)
        cv2.waitKey(1)

        if ret == False:
            print("No image found")

        if ret == True:
            # im = processImg(im)
            # find objects within current frame
            fgMask = backSub.apply(im, None, 0.0)
            # fgMask = processMask(fgMask)
            if DEBUG:
                cv2.imshow('cur mask', fgMask)
                cv2.waitKey(1)


            # for Blob detector processing:
            # detector = getBlobDetect()
            # im_with_keypoints, centroids = detectFrame_Blob(detector, im)

            im_with_keypoints, centroids = detectFrame_MOG(fgMask, im)


            for synth in all_synths:
                synth.resetModify()

            updateSynths(centroids)

            if heatmap_en:
                updateHeatmap(heatmapData)

            cv2.imshow("Keypoints", im)
            cv2.waitKey(1)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    for i in all_players:
        i.stop()


# example code for using smoother transitions:
# freqRamp = line(3 * s, freqStream.peek(), 850)
# gainRamp = line(3 * s, gainStream.peek(), dB2magnitude(freq2dB(850)) / maxgain)
# print("upper = " + str(dB2magnitude(freq2dB(850)) / maxgain))
# freqIter.append(freqRamp)
# gainIter.append(gainRamp)
