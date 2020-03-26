#!/usr/bin/env python3
import itertools
import synthIter as SI
import time
from audiolazy import *
import numpy as np

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


# testgain = ControlStream(1)
# testgain.add(line(2 * s, 1, 4))
# t_end = time.time() + 2
# while time.time() < t_end:
#     print(str(testgain.take(1)))


#           TESTING NEW ITER:
#   - start synthiter with given value
#   - continually return this for 2 seconds
#   - generate line and append to the synthiter
#   - return values for 2 sec

# synIter = SI.SynthIter(1.11123)
# a = np.array([2,3,4,5])
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# synIter.append(a)
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# synIter.append(a)
# print(synIter.peek())
# print(synIter.values())
# synIter.remove(20)
# print(synIter.values())
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))
# print(next(synIter))

testgain = SI.SynthIter(0)
teststream = Stream(testgain)
sine = sinusoid(1e3 * Hz * 1.25 + teststream)
t_end = time.time() + 2
maxValue = 0
minValue = 0
while time.time() < t_end:
    curValue = sine.take(1)[0]
    if curValue > maxValue:
        maxValue = curValue
    if curValue < minValue:
        minValue = curValue

print("MAX: " + str(maxValue))
print("MIN: " + str(minValue))

newvalues = line(2 * s, 0, 0.8)
testgain.append(newvalues)
t_end = time.time() + 2
while time.time() < t_end:
    curValue = sine.take(1)[0]
    if curValue > maxValue:
        maxValue = curValue
    if curValue < minValue:
        minValue = curValue
print("MAX: " + str(maxValue))
print("MIN: " + str(minValue))




# gimme space
