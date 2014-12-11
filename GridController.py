from GridWorker import GridWorker
from itertools import chain, izip

'''
Gridcontroller.py

take a single frame from a source and pipe it to the LED bridges

double buffered with only diffs being sent to lights

'''

class GridController:

   

    def __init__(self, width, height, testmode = False):
        print "creating gridcontroller of %ix%i" %(width, height)
        self.width = width
        self.height = height
        f1 = [[0,0,0] for a in range(0, width*height)]
        f2 = [[0,0,0] for a in range(0, width*height)]
        self.framebuffer = [f1, f2]
        self.activeBuffer = 0
        self.calibrationMap = []
        self.stationBulbMap = {}
        self.workerList = {}
        self.fastMode = False
        self.testmode = testmode

    def setFastMode(self):
        self.fastMode = True
        print "Using fast mode updates, uploading patterns now.."

    '''generate a list of pixel indices that have changed since last frame 
        returns [ index, value ] for each changed pixel 
    '''
    def generateDifferenceList(self):
        ret = []
        for ind in range(self.width * self.height):
            curValue = self.framebuffer[self.activeBuffer][ind] 
            prevValue = self.framebuffer[1-self.activeBuffer][ind]
            if prevValue != curValue :
                changedValue = curValue[:]

                #now check to see if the brightness level has changed between frames
                #if it hasnt then set the bri value to None
                if curValue[2] == prevValue[2]:
                    changedValue[2] = None
                if curValue[1] == prevValue[1]:
                    changedValue[1] = None 
                ret.append([ind, changedValue])
        
        #reverse the difference list. This will cause right hand LEDs to receive their updates before the left ones.
        # this makes scrolling text suck less
        ret = ret[::-1]

        return ret

    '''load the calibration map from given path
       and generate a sending thread for each unique base station IP
    '''
    def loadCalibrationMap(self, path):
        baseStationList = []
        f = open(path, 'r')
        for line in f:
            if line[0] != '#':
                parts = line.split(",")
                station = parts[0]
                bulbId = int(parts[1])
                self.calibrationMap.append( [station, bulbId])
                if station not in baseStationList:
                    baseStationList.append(station)
                    self.stationBulbMap[station] = []
                self.stationBulbMap[station].append(bulbId)
        print "loaded %i pixels from calibmap" % ( len(self.calibrationMap))
        print "generating worker threads.."
        #generate the worker threads for each 
        for station in baseStationList:
            w = GridWorker(station, testMode = self.testmode)
            self.workerList[station] = w
            if self.fastMode == True:
                print "uploading pointsymbols"
                w.fastMode = True
                w.sendPointSymbols(self.stationBulbMap[station])
            w.start()
            print "worker for %s started" % (w.stationIP)


    def stop(self):
        #turn off all the bulbs here
        #stop the threads
        for k in self.workerList.keys():
            w = self.workerList[k]
            print "stopping worker for %s" % (w.stationIP)
            w.end()
            w.join()


    '''
    receive new frame data into the currently not displayed buffer
    '''
    def newFrameData(self, data):
        if len(data) != self.width * self.height:
            print "Error!: new frame size incorrect",len(data)
            return
        #write into non-displayed buffer
        self.framebuffer[1-self.activeBuffer] = data[:]
        #switch buffer pointer
        self.activeBuffer = 1-self.activeBuffer
        self.flip()

    '''
    start sending the current buffer to the lights
    '''
    def flip(self):
        print "sending frame %i" % (self.activeBuffer)
        #generate a difference list
        diffList = self.generateDifferenceList()
        updateList = {} #list of updates to make per worker thread
        for w in self.workerList.keys():
            updateList[w] = []
        
        #grab the changes from the difference list and for reach create a bulbid,value pair
        for pair in diffList:
            pixelIndex, value = pair
            print pixelIndex
            baseStation, bulbId = self.calibrationMap[pixelIndex]
            updateList[baseStation] += [ [bulbId, value]]

        #push each workers updatelist entry to the worker then mark the frame as done
        for w in self.workerList.keys():
            #do any pixel order manipulations here
            #in this alternate between pairs of left and right leds 

            self.workerList[w].addData( updateList[w] )
            self.workerList[w].frameDone()

        #old update method in case above is fucked up
        """
        for pair in diffList:
            #look up the correct base station id for this bulb
            pixelIndex, value = pair
            baseStation, bulbId = self.calibrationMap[pixelIndex]
            worker = self.workerList[baseStation]
            worker.addData( [[bulbId , value]] )
        for w in self.workerList.keys():
            self.workerList[w].frameDone()
        """    







            















