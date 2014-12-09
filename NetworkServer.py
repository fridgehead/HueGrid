from GridController import GridController
import socket,sys



pallette = [40000, 7000, 14000, 21000, 28000, 35000, 42000, 49000]
bri = [0,255,255,255,255,255,255,255]
fastMode = False
w = 14
h = 12


import signal

def signal_handler(sig, frame):
  print("")
  g.stop()
  
  exit(0)

signal.signal(signal.SIGINT, signal_handler)


g = GridController(14, 12)

if fastMode :
    g.setFastMode()
g.loadCalibrationMap("test.map")
buffer = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.1.150", 9001))
#sock.setblocking(0)
#sock.bind(("127.0.0.1",9001))
blankFrame = [ [1,255,255] for a in range(w*h) ]
print "clearing to default"
g.newFrameData(blankFrame)
print "listening.."
while True:
    data = []
    buffer, addr = sock.recvfrom(1024)
    print "new frame"
    if len(buffer) != w * h:
        print ("WRONG SIZE" + str(w*h))
    else:
        # convert each element of buffer into 0-8 vals
        # fastmode ignores sat and val elements
        if fastMode:
            for a in buffer:
                print a
                if a == b'\x00':
                 
                    data.append([0,0,0])
                elif a == b'\x01':
                    data.append([1,0,0])
                elif a == b'\x02':
                    data.append([2,0,0])
                elif a == b'\x03':
                    data.append([3,0,0])
                elif a == b'\x04':
                    data.append([4,0,0])

                elif a == b'\x05':
                    data.append([5,0,0])

                elif a == b'\x06':
                    data.append([6,0,0])

                elif a == b'\x07':
                    data.append([7,0,0])

                elif a == b'\x08':
                    data.append([8,0,0])






        else:
            for a in buffer:
                ind = ord(a)
                colour = pallette [ind]

                data.append([colour,255 , bri[ind]])
            
        g.newFrameData(data)


