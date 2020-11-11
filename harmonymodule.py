#!/usr/bin/env python3
from synthmodule    import *
# ^ should give acess to all_synths
# methods for determining whether current frequencies are in harmony

# TODO:
# make function that returns whether given synths are in harmony

def harmonious_synths():

    # in: array of frequencies

    # not sure how to output indices corresponding to harmonious synths,
    # instead will just update gain here!

    # find how many synths are harmonious
    #   if a set of harmonious synths already exists:
    #       check if set is still harmonious
    #           if it is, keep it and proceed to next steps
    #           if it isn't, discard set and proceed to "if there is no set"
    #       skip ones in that set, only testing other synths
    #       (will need set of harmonious synths to be persistent!!)

    #   if there is no current set of harmonious synths:
    #       for each synth, see if it is harmonious with other synths
    #           only look at synths outside of the current set of synths
    #           divide it's frequency by frequency of other synths
    #               (whichever one is largest is in denominator)
    #           if within threshold, the two are harmonious!
    #           create set of the two synths and be done (check for set existence every time)



    #       note: if a harmonious with b, c harmonious with synth b,
    #       then a harmonious with c AKA it is communicative
    #           -> make a bunch of sets


    # aplify those harmonious synths specifically
    #   more harmonious synths -> each one is amplified more

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
    # like that leetcode problem: find number of elements in array that add up to target value!
    # here, find number of elements in array that are a "good" multiple of each other
    print('yeet')
