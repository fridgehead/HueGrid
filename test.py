from GridController import GridController
from time import sleep
import socket

try:
    g = GridController(2, 2, testmode = True)
    g.setFastMode()
    g.loadCalibrationMap("test.map")
    i = 0
    while True:
        data = [[10000,255,255] for a in range(0,4)]
        data[i][0] = 1
        data[(i+1) %4 ][0] = 2
        print i
        g.newFrameData(data)
        sleep(0.5)
except KeyboardInterrupt:
    print "Stopping..."
    g.stop()




