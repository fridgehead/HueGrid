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
    g = GridController(1, 5, testmode = True)
    #g.setFastMode()
    g.loadCalibrationMap("test.map")
    i = 1
    data = range(0,5)
    di = 1
    while True:
        for c in range (0, 5):
            data[c] = [0, 255,255 ]
        data[i] = [3, 255,255 ]

        i += 1
        i %= 5 
        g.newFrameData(data)
        sleep(3.5)
except KeyboardInterrupt:
    print "Stopping..."
    g.stop()




