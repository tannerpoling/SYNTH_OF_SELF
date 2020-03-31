#!/usr/bin/env python3
from audiolazy import *
import time
import threading
import synthIter as SI

def dB2magnitude(logpower):
  return 10 ** (logpower / 20)

intensity = 50 # phons
freq2dB = phon2dB.iso226(intensity)

class MySynth:
    # Synth fields:
    # each synth has 3 iters in it:
    #   freqIter -> frequency of sinusoid driving synth
    #       freqStream (stream based on freqIter)
    #   gainIter -> base gain of synth, changes with frequency to keep volume consistent
    #       gainStream (stream based on gainIter)
    #   modIter  -> frequency of modulator modifying synth volume
    #       modStream (stream based on modIter)
    # all except gainIter have a min/max, values that should be held by the program using this,
    # passed in construction

    # flag for whether it's been modified in the last cycle (aka if object has disappeared)

    # Useful functions:
    #   changeFrequency(newValue in Hz)
    #       this automatically changes gain as well
    #   changeGain(newValue in Hz -> converted to whatever units)
    #       if we want to map gain to something later
    #   changeMod(newValue in Hz)
    #
    # !!!! NEED TO GET MAXGAIN VALUE AS JUST A NUMBER AND SAVE AS VARIABLE IN HERE

    def __init__(self, initFreq = 0, initGain = 0, initMod = 0):
        self.initFreq = initFreq
        self.initGain = initGain
        self.initMod = initMod
        self.freqIter = SI.SynthIter(self.initFreq)
        self.freqStream = Stream(self.freqIter)
        self.gainIter = SI.SynthIter(self.initGain)
        self.gainStream = Stream(self.gainIter)
        self.modIter = SI.SynthIter(self.initMod)
        self.modStream = Stream(self.modIter)
        self.modified = True
        return self

    # assumes that given frequency has been fixed, converted from openCV coord range -> freq range
    def changeFreq(self, newFreq):
        self.freqIter.changeValue(newFreq)
        self.gainIter.changeValue(dB2magnitude(freq2dB(newFreq)) / maxgain) # FIX THIS
        self.modified = True

    # assumes that given value is a frequency value that has been converted already
    def changeMod(self, newMod):
        self.modIter.changeValue(newMod)
        self.modified = True

    # set 'modified' flag to false
    def resetModify(self):
        self.modified = False

    # set volume to zero if synth hasn't been modfied (AKA num objects < num synths)
    def checkModify(self):
        if self.modified == False:
            self.gainIter.changeValue(0)
