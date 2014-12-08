from threading import Thread
from Queue import Queue
from time import sleep
from phue import Bridge
import json


class GridWorker(Thread):

    def __init__(self, stationIP, testMode = True):
        Thread.__init__(self)
        self.stationIP = stationIP
        self.queue = Queue()
        self.testMode = testMode
        if testMode != True:
            self.bridge = Bridge(ip=stationIP, username="newdeveloper")
       
        self.transitionTime = 1
        self.running = True
        self.fastMode = False
        self.fastModeReady = False

        self.frameReady = False

    def end(self):
        self.running = False
        self.queue.join()

    ''' take list of bulb ids and colour values, add to queue '''
    def addData(self, dataList):
        if self.fastMode == True and self.fastModeReady == False:
            return
        for item in dataList:
            self.queue.put(item)

    def frameDone (self):
        self.frameReady = True

    def run(self):
        while self.running:
            #read from queue
            if self.fastMode == True:
                self.doFastMode()
            else :
                self.slowMode()

    def doFastMode(self):
        if self.frameReady == False:
            return
        #here the value represents a colour index from the shitty pallette
        #read the queue until empty or 16 have been read
        bulbList = []
        valueList = []
        ct = 0
        doUpdate = False
        while self.queue.empty() == False and ct < 16:
            bulbId, value = self.queue.get(False)
            value = value[0]
            bulbList.append(bulbId)
            valueList.append(value)
            ct += 1
            doUpdate = True
            self.queue.task_done()
	if doUpdate == True and self.testMode == False:
            print 
            #run over the upates in bulb list and compile them into the weird format it needs
            cmd = [01, 01]
            cmd.append(len(valueList))
            for i in range(0, len(bulbList)):
                cmd.append(valueList[i])
                cmd.append(bulbList[i])
            print cmd    
            cmdString = str(bytearray(cmd)).encode('hex')
            command = {"duration" : 10000, "symbolselection" : cmdString}
            self.bridge.request('PUT', '/api/' + self.bridge.username + '/groups/0/transmitsymbol', json.dumps(command))
            sleep(0.05)

        if self.queue.empty():
            self.frameReady = False


    def slowMode(self):
        if self.queue.empty() == False:
            bulbId, value = self.queue.get(False)
            #send to base station
            command = {'hue' : value[0], 'sat' : value[1], 'bri' : value[2], 'transitiontime' : self.transitionTime} 
            if self.testMode != True:
                self.bridge.set_light(bulbId, command)
            else :
                print "command " + str(command)
            sleep(0.32)                
            self.queue.task_done()
    
    def sendPointSymbols(self, lightList):
        col = range(0,7)
        col[0] = "320000002A10101000FF"
        col[1] = "320000002A65FF7F00FF"
        col[2] = "320000002AFF060000FF"
        col[3] = "320000002AE52A0200FF"
        col[4] = "320000002A0AFF1100FF"
        col[5] = "320000002A0DFFC200FF"
        col[6] = "320000002A0300C700FF"
        command = {}
        for i in range(0, 7):
            command[str(i+1)] = col[i]
        for i, light in enumerate(lightList):
            if self.testMode == False:
                self.bridge.request('PUT', '/api/' + self.bridge.username + '/lights/' + str(i+1) + '/pointsymbol', json.dumps(command))
            sleep(0.54)
        print "..upload complete"
        self.fastModeReady = True
      

