from GridController import GridController
from time import sleep
import socket

col = [ [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [3, 255, 255],
        [4, 255, 255],
        [5, 255, 255],
        [6, 0, 0]]


try:
    g = GridController(13, 1)
    g.setFastMode()
    g.loadCalibrationMap("test.map")
    i = 1
    data = range(0,13)
    di = 1
    while True:
        for c in range (0, 13):
            data[c] = [1, 255,255 ]
        data[i] = [3, 255,255 ]

        i += di

        if i >= 13:
            i = 12
            di = -1
        elif i <= 0:
            i = 0;
            di = 1


        g.newFrameData(data)
        sleep(0.5)
except KeyboardInterrupt:
    print "Stopping..."
    g.stop()




