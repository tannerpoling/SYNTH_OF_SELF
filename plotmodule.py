#!/usr/bin/env python3
# for plotting heatmap of object coordinates
import matplotlib.pyplot as plt
import numpy as np

# how this will work:
#   - have a graphing flag to distinguish graphing bits of code
#   - in synthofself: append coords of detected objects to arrays
#       of x and y values
#   - convert list of coords to heatmap via matplotlib
#   - use animate function in matplotlib to update heatmap in real time
#   - add option of saving output / logs

# TODO:
# - make init method, create data structures needed for heatmap generation
# - visualzation method (will inform what data structures we need)

first = True
fig = plt.figure()
ax = fig.add_subplot(111)
im = None
im = ax.imshow(np.random.random((50,50)))
plt.show(block=False)

def updateHeatmap(heatmapData):
    global first
    global im
    global ax
    global fig
    # x = heatmapData[:][0]
    # y = heatmapData[:][1]
    # plt.imshow(heatmapData, cmap='hot', interpolation='nearest')

    if first:
        im = ax.imshow(heatmapData, cmap='hot', interpolation='nearest')
        # plt.show()
        first = False
    else:
        im.set_array(heatmapData)

    fig.canvas.draw()
