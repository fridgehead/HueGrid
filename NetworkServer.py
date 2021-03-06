
"""
Server.py - Interface to Tom's Hue Grid Code, Ben's 
 LED Board and a test window
author : Tom Wyatt / Benjamin Blundell
email : tom@imakethin.gs / oni@section9.co.uk
"""

import socket, argparse, sys, time

class GridServer:

  def __init__(self, ipaddr="localhost", port=9001, bufferx=14, buffery=13, rate=2.0):

    self.bufferX = bufferx
    self.bufferY = buffery
    self.ipaddr = ipaddr
    self.port = port
    self.rate = rate # in seconds for updates
    self.running = False
    

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
    recv_buffer_size = self.bufferY * self.bufferX

    while self.running:

      # TODO - Should we wait for data or be changing the screen
      # at a regular rate? I think the latter
      received_buffer = []
      try:
        received_buffer = self.sock.recv(2048) # We assume that bufferx * buffery is less than this number
        received_buffer.strip()
      except socket.error:
        # Likely there was no data as we are non blocking
        pass  
        
      if len(received_buffer) == recv_buffer_size:

      # Our serial buffer is actually 30 x 30 x 3
      # We need to pad it out

        ridx = 0

        for i in reversed(range(0,30)):
          iw = i * 30 * 3

          if i < self.bufferY:
            for j in range(0,30):
              if j < self.bufferX:
                (r,g,b) = palette[int(received_buffer[ridx])]      
                self.led_data[iw + j * 3 ] = b
                self.led_data[iw + j * 3 + 1] = r
                self.led_data[iw + j * 3 + 2] = g

                ridx += 1
              else:
                self.led_data[iw + j * 3 ] = 0
                self.led_data[iw + j * 3 + 1] = 0
                self.led_data[iw + j * 3 + 2] = 0

          # Check against rate limit - dont overload
          now = time.time()
          dt = now - self.start_time 
          if dt >= self.rate:
            self.start_time = now # Be careful where you put this
            serial_comms.set_image(self.led_data,self.ser)

    self.ser.close()
    self.sock.close()

  def quit(self):
    self.ser.close()
    self.sock.close()
    self.running = False

  def test(self,game,wrapper):
    ''' Run the test server showing the game on screen with pygame '''

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

    # Create a temporary test palette for ourselves
    buffer_palette = {0 : 0, 1 : "I", 2 : "J", 3 : "L" , 4 : "O", 5 : "Z", 6 : "S", 7 : "T" }

    print ("Running server at: " + self.ipaddr + " on port: " + str(self.port) )

    self.start_time = time.time()
    recv_buffer_size = self.bufferY * self.bufferX

    self.running = True

    wrapper.init()

    while self.running:

      wrapper.frame()

      # TODO - Should we wait for data or be changing the screen
      # at a regular rate? I think the latter
      received_buffer = []
      try:
        received_buffer = self.sock.recv(1024) # We assume that bufferx * buffery is less than this number
        received_buffer.strip()

      except socket.error:
        # Likely there was no data as we are non blocking
        pass  
      
      if len(received_buffer) == recv_buffer_size:

        now = time.time()
        dt = now - self.start_time 
        if dt >= self.rate:
          self.start_time = now # Be careful where you put this
          # I ALWAYS forget about ord ><
          game.copyLinearBufferReversed( [ buffer_palette[ ord(b) ] for b in received_buffer] )

    # Finished so cleanup
    wrapper.cleanup()
     

  def mapData(self, sentbyte, fastmode=False):
    ''' Given a byte from the data stream run the conversion for Tom's stuff.'''
    
    # This could need testing - fastmode
    if fastmode:
      return [ord(sentbyte),0,0]

    palette = [40000, 7000, 14000, 21000, 28000, 35000, 42000, 49000]
    bri = [0,255,255,255,255,255,255,255]
    sat = [255,255,255,255,255,255,255,0]

    ind = ord(sentbyte)
    colour = palette [ind]
    #drop the saturation value as its already set to 255 by the gridworker at startup
    return [colour, sat[ind], bri[ind]]


  def run(self, fastmode):
    ''' Run round the sever, listening for udp packets and sending
    the data to the grid controller. We perform a restriction on how
    fast we call the grid-controller but we can receive very quickly.'''

    from GridController import GridController

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

    self._g = GridController(self.bufferX, self.bufferY, testmode = False)

    if fastmode:
      self._g.setFastMode()

    self._g.loadCalibrationMap("test.map")

  
    self.start_time = time.time()
    recv_buffer_size = self.bufferY * self.bufferX

    # Blank out first
    blankFrame = [ [0,255,0] for a in range(recv_buffer_size) ]
    print "clearing to default"
    self._g.newFrameData(blankFrame)


    # Now actually run the server listening for frames

    self.running = True
    while self.running:

      # TODO - Should we wait for data or be changing the screen
      # at a regular rate? I think the latter
      received_buffer = []
      try:
        received_buffer = self.sock.recv(1024) # We assume that bufferx * buffery is less than this number
        received_buffer.strip()
      except socket.error:
        # Likely there was no data as we are non blocking
        pass  
      
      if len(received_buffer) == recv_buffer_size:
        now = time.time()
        dt = now - self.start_time 
        if dt >= self.rate:
          self.start_time = now # Be careful where you put this

          # convert each element of buffer into 0-8 vals
          # fastmode ignores sat and val elements 
          data = [ self.mapData(a) for a in received_buffer]
          self._g.newFrameData(data)


    self._g.stop()


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
  parser.add_argument('--fastmode', help='do we want fastmode.', action='store_true')
  parser.add_argument('--test', help='Run in test mode with pygame', action='store_true')

  argz = vars(parser.parse_args())

  width = 14 
  height = 13
  addr = "127.0.0.1"
  port = 9001
  rate = 2.0
  fastmode = False

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

  if argz["fastmode"]:
    fastmode = argz["fastmode"]

  server = GridServer(addr, port, width, height, rate)

  if argz["test"]:

    import pygame_wrapper, pygame, buffergame

    bb = buffergame.BufferGame(width,height)
    wrapper = pygame_wrapper.Wrapper(bb.buffer, bb.boardX, bb.boardY)

    server.test(bb,wrapper)
  
  else:
    server.run(fastmode)

