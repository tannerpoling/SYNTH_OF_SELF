#!/usr/bin/env python3
import itertools
import synthIter as SI
import time

a = [1, 2, 3]

# for element in itertools.cycle(a):
#     print(str(element))

synIter = SI.SynthIter(0.15)
test = iter(synIter)
t_end = time.time() + 5
while time.time() < t_end:
    print(str(next(test)))
