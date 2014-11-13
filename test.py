from GridController import GridController
from time import sleep

try:
    g = GridController(2, 2)
    g.setFastMode()
    g.loadCalibrationMap("test.map")
    i = 0
    while True:
        i += 1
        i = i % 4
        data = [[10000,255,255] for a in range(0,4)]
        data[i][0] = 10000
        data[(i+1) %4 ][0] = 20055
        print i
        g.newFrameData(data)
        sleep(0.5)
except KeyboardInterrupt:
    print "Stopping..."
    g.stop()




