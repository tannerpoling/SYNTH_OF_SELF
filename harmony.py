#!/usr/bin/env python3

# methods for determining whether current frequencies are in harmony

# TODO:
# make function that returns whether given synths are in harmony

def harmony(freqs):
    # return true if current synths are within harmony
    # pass in all synths? or assume global access

    # in: array of frequencies
    # should harmony be a boolean? int range of 0 to 255?
    # idea: array sorted from lowest to highest frequency
    #
    # notes on listening to random frequencies
    # listening to base of 225
    # 1 = 225, .5 = 112.5, .25 = 56.25, .125 = 28.125
    # 1/3 = 75
    # good: 1 + 1.5 + 2 + 2.5 + ... (halves always good)
    #  ^^   225 + 338 + 450 + 563
    #       1 + 1.25 + 1.5 (+ 1.75 BAD)
    #       1 + 1.125 BAD
    #       1 + 1.3 + 1.6 + 2 + ... (thirds always good)
    # (multipliers of base frequency / lowest frequency)


    # assume first index is the base?
    # like that leetcoe problem: find number of elements in array that add up to target value!
    # here, find number of elements in array that are a "good" multiple of each other
