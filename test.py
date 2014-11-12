from GridController import GridController
from time import sleep

try:
    g = GridController(1, 4)
    g.loadCalibrationMap("test.map")
    i = 0
    while True:
        i += 1
        data = [0,0,0,0]
        data[i %4] = 255
        g.newFrameData(data)
        sleep(2)
except KeyboardInterrupt:
    print "Stopping..."
    g.stop()




