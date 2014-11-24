"""
Server.py - Interface to Tom's Hue Grid Code and Ben's LED Board
author : Tom Wyatt / Benjamin Blundell
email : tom@imakethin.gs / oni@section9.co.uk

"""

import socket, argparse, sys, time


class GridServer:

  def __init__(self, ipaddr="localhost", port=9001, bufferx=2, buffery=2, rate=2.0):

    self.bufferX = bufferx
    self.bufferY = buffery

    self.ipaddr = ipaddr
    self.port = port
    self.rate = rate # in seconds for updates
    

  def run_led(self):
    ''' A test function for the LED wall in the office. Similar to the 
    run() functon but does a few more checks here and calls our serialcoms '''
    import serial_comms

    self.ser = serial_comms.connect()

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
      self.sock.bind((self.ipaddr, self.port))
      # TODO - pick the right exception
    except:
      print("Failure to bind.")
      self.sock.close()
      raise
      self.sock.setblocking(0)

    self.sock.setblocking(0)

    led_buffer_size = 30 * 30 * 3

    # Create our LED Buffer - 30 * 30 RGB LEDs
    self.led_data = []
    for i in range(0, led_buffer_size):
      self.led_data.append(0)
    
    self.running = True

    palette = { 0: (0,0,0), 1: (255,0,0), 2 : (255,255,0), 3:(255,0,255), 
      4: (0,255,0), 5:(0,255,255), 6:(0,0,255), 7:(255,255,255) }

    print ("Running server at: " + self.ipaddr + " on port: " + str(self.port) )

    self.start_time = time.time()

    while self.running:

      # TODO - Should we wait for data or be changing the screen
      # at a regular rate? I think the latter
      
      try:
        recv_buffer_size = self.bufferY * self.bufferX
        received_buffer = self.sock.recv(512) # We assume that bufferx * buffery is less than this number
        received_buffer = received_buffer.strip()

        #print("received frame")
        
        if len(received_buffer) != recv_buffer_size:
          print("Buffer receieved is the wrong size: " + str(len(received_buffer)) + " vs " + str(self.bufferY * self.bufferX))
          continue # Perhaps not the best option

        # Our serial buffer is actually 30 x 30 x 3
        # We need to pad it out
        
        # Clear Data buffer
        for i in range(0, led_buffer_size):
          self.led_data[i] = 0

        idx = 0
        ridx = 0
   
        for i in reversed(range(0,30)):
          if i < self.bufferY:
            for j in range(0,30):
              if j < self.bufferX:
                (r,g,b) = palette[int(received_buffer[ridx])]

                self.led_data[idx*3] = b
                self.led_data[idx*3 + 1] = r
                self.led_data[idx*3 + 2] = g
              
                ridx+=1
              idx += 1
      except socket.error:
        # Likely there was no data as we are non blocking
        pass

      # Check against rate limit - dont overload
      now = time.time()
      dt = now - self.start_time 
      if dt >= self.rate:
        self.start_time = now # Be careful where you put this
        #print("Setting Screen")
        serial_comms.set_image(self.led_data,self.ser)
        
     
    self.ser.close()
    self.sock.close()

  def quit(self):
    self.ser.close()
    self.sock.close()

  def run(self):
    ''' Run round the sever, listening for udp packets and sending
    the data to the grid controller. We perform a restriction on how
    fast we call the grid-controller but we can receive very quickly.'''

    from GridController import GridController

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

  import signal

  def signal_handler(sig, frame):
    print("Quitting Server.")
    server.quit()
    sys.exit(0)

  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--width', metavar='N', type=int, help='buffer width.')
  parser.add_argument('--height', metavar='N', type=int, help='buffer height.')
  parser.add_argument('--addr', metavar='ip address', help='ip address to bind to.')
  parser.add_argument('--port', metavar='N', type=int, help='port to listen on.')
  parser.add_argument('--rate', metavar='N', type=float, help='refresh rate in seconds.')

  argz = vars(parser.parse_args())

  width = height = 2
  addr = "127.0.0.1"
  port = 9001
  rate = 2.0

  if argz["width"]:
    width = argz["width"]

  if argz["height"]:
    height = argz["height"] 

  if argz["addr"]:
    addr = argz["addr"]

  if argz["port"]:
    port = argz["port"] 

  if argz["rate"]:
    rate = argz["rate"]


  server = GridServer(addr, port, width, height, rate)
  server.run_led()

