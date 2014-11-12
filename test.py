from GridController import GridController
from time import sleep

try:
    g = GridController(1, 4)
    g.loadCalibrationMap("test.map")
    while True:

        g.newFrameData([255,254,253,252])
        sleep(2)
except KeyboardInterrupt:
    print "Stopping..."
    g.stop()




