import socket
from GridController import GridController

pallette = [0, 7000, 14000, 21000, 28000, 35000, 42000, 49000]

ip = "127.0.0.1"
port = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

fastMode = True

try:
    g = GridController(2, 2)
    if fastMode :
        g.setFastMode()
    g.loadCalibrationMap("test.map")
    buffer = []
    while True:
	buffer, addr = sock.recvfrom(1024)
	print "new frame"
	if len(buffer) != w * h:
		print "WRONG SIZE"
	else:
		# convert each element of buffer into 0-8 vals
		# fastmode ignores sat and val elements 
                if fastMode:
                    data = [[a,0,0] for a in buffer]
                else:
                    data = [[pallette[a%8],255,255] for a in buffer]
		g.newFrameData(data)

except KeyboardInterrupt:
    print "Stopping..."
    g.stop()
