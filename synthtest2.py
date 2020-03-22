#!/usr/bin/env python3
from audiolazy import *
import time
import threading


if PYTHON2:
  input = raw_input

rate = 44100 # samples/s
fstart, fend = 16, 20000 # Hz
intensity = 50 # phons
chirp_duration = 5 # seconds
total_duration = 9 # seconds

DEBUG = True

# assert just checks that something is true, throwing error otherwise
assert total_duration > chirp_duration

def finalize(zeros_dur):
  print("Finished!")
  for el in zeros(zeros_dur):
    # yield allows you to return a SEQUENCE of values rather than a singular return.
    # used in generator functions: these functions can store state data and use it
    # in subsequent calls! pretty cool
    yield el

def dB2magnitude(logpower):
  return 10 ** (logpower / 20)

def playTone2(duration):
    th2 = player.play(sinusoid(1e3 * Hz * 2) * refgain)
    time.sleep(duration)
    th2.stop()


def changingFreq():
    freq = 1e3 * Hz
    while True:
        time.sleep(0.1)
        freq = freq + 100


s, Hz = sHz(rate)
freq2dB = phon2dB.iso226(intensity)

freq = 1e3 * Hz

freq = thub(2 ** line(chirp_duration * s, log2(fstart), log2(fend)), 2)
gain = thub(dB2magnitude(freq2dB(freq)), 2)
maxgain = max(gain)

unclick_dur = rint((total_duration - chirp_duration) * s / 2)
gstart = line(unclick_dur, 0, dB2magnitude(freq2dB(fstart)) / maxgain)
gend = line(unclick_dur, dB2magnitude(freq2dB(fend)) / maxgain, 0)

sfreq = chain(repeat(fstart, unclick_dur), freq, repeat(fend, unclick_dur))
sgain = chain(gstart, gain / maxgain, gend)

snd = sinusoid(sfreq * Hz) * sgain

with AudioIO(True) as player:
  refgain = dB2magnitude(freq2dB(1e3)) / maxgain
  # th = player.play(sinusoid(1e3 * Hz) * refgain)
  th = player.play(sinusoid(freq) * refgain)

  input("Playing the 1 kHz reference tone. You should calibrate the output "
        "to get {0} dB SPL and press enter to continue.".format(intensity))
  playTone2(2)
  th.stop()
  print("Playing the chirp!")
  player.play(chain(snd, finalize(.5 * s)), rate=rate)
