from threading import Thread
from Queue import Queue


class GridWorker(Thread):

    def __init__(self, stationIP):
        Thread.__init__(self)
        self.stationIP = stationIP
        self.queue = Queue()
        self.running = True

    def end(self):
        self.running = False
        self.queue.join()

    ''' take list of bulb ids and colour values, add to queue '''
    def addData(self, dataList):
        for item in dataList:
            self.queue.add(item)

    def run(self):
        while self.running:
            #read from queue
            if self.queue.empty() == False:
                bulbValuePair = self.queue.get(False)
                print "station %s setting id %i to value %i" %(self.stationIP, bulbValuePair[0], bulbValuePair[1])
                #send to base station
                self.queue.task_done()


