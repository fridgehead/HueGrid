from threading import Thread
from Queue import Queue
from time import sleep
from phue import Bridge


class GridWorker(Thread):

    def __init__(self, stationIP, testMode = True):
        Thread.__init__(self)
        self.stationIP = stationIP
        self.queue = Queue()
        self.testMode = testMode
        if testMode != True:
            self.bridge = Bridge(stationIP)
        
        self.running = True

    def end(self):
        self.running = False
        self.queue.join()

    ''' take list of bulb ids and colour values, add to queue '''
    def addData(self, dataList):
        for item in dataList:
            self.queue.put(item)

    def run(self):
        while self.running:
            #read from queue
            if self.queue.empty() == False:
                bulbId, value = self.queue.get(False)
                print "station %s setting id %s to value %s" %(self.stationIP, bulbId, value)
                #send to base station
                if self.testMode != True:
                    b.set_light(bulbId, 'bri', value, transitiontime=1)
                sleep(0.3)                
                self.queue.task_done()


