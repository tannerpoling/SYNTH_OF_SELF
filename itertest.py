#!/usr/bin/env python3
import itertools

a = [1, 2, 3]

for element in itertools.cycle(a):
    print(str(element))
