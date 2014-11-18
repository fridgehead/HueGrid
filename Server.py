import socket
from GridController import GridController

w = 2
h = 2

ip = "127.0.0.1"
port = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))


try:
    g = GridController(w, h, testmode = True)
    g.setFastMode()
    g.loadCalibrationMap("test.map")
    buffer = []
    while True:
	buffer, addr = sock.recvfrom(1024)
	buffer = buffer.strip()
	print "new frame"
	if len(buffer) != w * h:
		print "WRONG SIZE"
	else:
		# convert each element of buffer into 0-8 vals
		# fastmode ignores sat and val elements 
		data = [[int(a),0,0] for a in buffer]
		g.newFrameData(data)

except KeyboardInterrupt:
    print "Stopping..."
    g.stop()
