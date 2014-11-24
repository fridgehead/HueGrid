"""
Server.py - Interface to Tom's Hue Grid Code and Ben's LED Board
author : Tom Wyatt / Benjamin Blundell
email : tom@imakethin.gs / oni@section9.co.uk

"""

import socket, argparse, sys
from GridController import GridController


class GridServer:

  def __init__(self, ipaddr="localhost", port=9001, bufferx=2, buffery=2):

    self.bufferX = bufferx
    self.bufferY = buffery

    self.ipaddr = ipaddr
    self.port = port
    

  def run_led(self):
    ''' A test function for the LED wall in the office. Similar to the 
    run() functon but does a few more checks here and calls our serialcoms '''
    import serial_comms

    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.sock.bind((self.ipaddr, self.port))

      #ser = serial_comms.connect()
      self.running = True

      palette = { 0: (0,0,0), 1: (255,0,0), 2 : (255,255,0), 3:(255,0,255), 
        4: (0,255,0), 5:(0,255,255), 6:(0,0,255), 7:(255,255,255) }

      print ("Running server at: " + self.ipaddr + " on port: " + str(self.port) )

      while self.running:
        received_buffer, addr = self.sock.recvfrom(1024)
        received_buffer = received_buffer.strip()
        
        print("new frame")
        
        if len(received_buffer) != self.bufferY * self.bufferX:
          print("WRONG SIZE")
        else:

          # Our serial buffer is actually 30 x 30 x 3
          # We need to pad it out

          idx = 0
          led_data = []

          for i in range(0,30):
            if i < self.bufferY:
              for j in range(0,30):
                if j < self.bufferX:
                  (r,g,b) = palette[received_buffer[idx]]
                  idx += 1
                  data = data + [b,r,g]
                else:
                  data = data + [0,0,0]

            else:
              for j in range(0,30):
                data = data + [0,0,0] # could be slow :S

          #serial_comms.set_image(led_data,ser)
       
      #ser.close()

    except: 
      import traceback
      print ("Error occured: " + sys.exc_info()[0])
      print (traceback.print_exc())

  

  def run(self):
    ''' Run round the sever, listening for udp packets and sending
    the data to the grid controller. We perform a restriction on how
    fast we call the grid-controller but we can receive very quickly.'''

    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.sock.bind((self.ipaddr, self.port))

      self._g = GridController(self.bufferX, self.bufferY, testmode = True)
      self._g.setFastMode()
      self._g.loadCalibrationMap("test.map")
      buffer = []

      self.running = True
      
      while self.running:
        buffer, addr = self.sock.recvfrom(1024)
        buffer = buffer.strip()
        
        print("new frame")
        
        if len(buffer) != self.bufferY * self.bufferX:
          print("WRONG SIZE")
        else:
        # convert each element of buffer into 0-8 vals
        # fastmode ignores sat and val elements 
          data = [[int(a),0,0] for a in buffer]
          self._g.newFrameData(data)

    except: 
      print("Error occured. Stopping.")
      self._g.stop()

  def stop():
    self._g.stop


if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--width', metavar='N', type=int, help='buffer width.')
  parser.add_argument('--height', metavar='N', type=int, help='buffer height.')
  parser.add_argument('--addr', metavar='ip address', help='ip address to bind to.')
  parser.add_argument('--port', metavar='N', type=int, help='port to listen on.')

  argz = vars(parser.parse_args())


  width = height = 2
  addr = "127.0.0.1"
  port = 9001

  if argz["width"]:
    width = argz["width"]

  if argz["height"]:
    width = argz["height"] 

  if argz["addr"]:
    addr = argz["addr"]

  if argz["port"]:
    port = argz["port"] 


  server = GridServer(addr, port, width, height)
  server.run_led()

