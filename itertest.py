#!/usr/bin/env python3
import itertools
import synthIter as SI
import time
from audiolazy import *

a = [1, 2, 3]

# for element in itertools.cycle(a):
#     print(str(element))

# synIter = SI.SynthIter(0.15)
# test = iter(synIter)
# t_end = time.time() + 5
# while time.time() < t_end:
#     print(str(next(test)))

rate = 44100 # samples/s
s, Hz = sHz(rate)


testgain = ControlStream(1)
testgain.add(line(2 * s, 1, 4))
t_end = time.time() + 2
while time.time() < t_end:
    print(str(testgain.take(1)))
