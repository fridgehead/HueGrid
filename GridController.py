from GridWorker import GridWorker

'''
Gridcontroller.py

take a single frame from a source and pipe it to the LED bridges

double buffered with only diffs being sent to lights

'''

class GridController:

    def __init__(self, width, height):
        print "creating gridcontroller of %ix%i" %(width, height)
        self.width = width
        self.height = height
        f1 = [0 for a in range(0, width*height)]
        f2 = [0 for a in range(0, width*height)]
        self.framebuffer = [f1, f2]
        self.framePtr = 0
        self.calibrationMap = []
        self.workerList = []

    '''generate a list of pixel indices that have changed since last frame '''
    def generateDiffList(self):
        ret = []
        for ind in range(self.width * self.height):
            if self.frameBuffer[framePtr] != self.frameBuffer[1-framePtr]:
                ret.append(ind)
        return ret

    '''load the calibration map from given path
       and generate a sending thread for each unique base station IP
    '''
    def loadCalibrationMap(self, path):
        baseStationList = []
        f = open(path, 'r')
        for line in f:
            parts = line.split(",")
            station = parts[0]
            bulbId = int(parts[1])
            self.calibrationMap.append( [station, bulbId])
            if station not in baseStationList:
                baseStationList.append(station)
        print "loaded %i pixels from calibmap" % ( len(self.calibrationMap))
        print "generating worker threads.."
        #generate the worker threads for each 
        for station in baseStationList:
            w = GridWorker(station)
            self.workerList.append(w)
            w.start()
            print "worker for %s started" % (w.stationIP)

    def stop(self):
        #turn off all the bulbs here
        #stop the threads
        for w in self.workerList:
            print "stopping worker for %s" % (w.stationIP)
            w.end()
            w.join()


    '''
    receive new frame data into the currently not displayed buffer
    '''
    def newFrameData(self, data):
        pass
    '''
    start sending the current buffer to the lights
    '''
    def flip(self):
        pass
