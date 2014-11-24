"""
game.py - base file for the tetris game
author : Benjamin Blundell
email : oni@section9.co.uk

"""

import tetris, argparse, time, sys, socket

class Game:

  ''' A game class that controls the timing and viewing of the game state
  This class also communicates with the server side '''

  def __init__(self, game, fps=2, local=True, server_address="192.168.1.1", port=9001, pygame=False):
    self.fps = fps;
    self.interval = 1 / fps;
    self.game = game
    self.pygame = pygame
    self.server_address = server_address
    self.port = port
    self.local = local

    self.buffer_palette = {'I' : 1, 'J' : 2, 'L' : 3, 'O' : 4, 'Z' : 5, 'S' : 6 , 'T' : 7 }
    
    if self.pygame:
      self.pygame.init()

    if not local:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


  def bufferToServer(self):
    ''' send the game buffer to the server via udp.
    We prepare the buffer by converting down into numnbers 0-8.'''

    try:
      send_buffer = [] 

      for item in self.game.getLinearBuffer():
        if item in self.buffer_palette.keys():
          send_buffer.append(self.buffer_palette[item])
        else:
          send_buffer.append(0)

      msg = ''.join(chr(x) for x in send_buffer)
      self.socket.sendto(msg, (self.server_address, self.port))

    except:
      import traceback
      print("Error connecting to server: " + self.server_address + ":" + str(self.port))
      print(traceback.print_exc())

  def sendBuffer(self):
    ''' package the buffer and send over udp '''
    pass


  def loop(self):
    start_time = time.time()
    self.running = True
    
    while self.running:
       
      # Cx pygame - kill it but keep the game running 
      if self.pygame:
        if self.pygame.running:
          self.pygame.frame()
        else:
          self.pygame.cleanup()
          self.pygame = False

      now = time.time()
      dt = now - start_time 
      if dt >= self.interval:
        
        self.game.frame(self.fps)
        #print("---")
        #self.game.prettyPrint()
        start_time = now

      if not self.local:
        self.bufferToServer()

  def quit(self):
    print("Quitting...")
    if self.pygame:
      self.pygame.cleanup()

    self.running = False
    sys.exit()


if __name__ == "__main__" : 

  import signal

  def signal_handler(sig, frame):
    print("")
    game.quit()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)
  print ('Launching Tetris...')
  print ('Press Ctrl+C to exit')

  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--fps', metavar='N', type=float, help='overall framerate.')
  parser.add_argument('--pygame', help='launch a pygame window.', action='store_true')
  parser.add_argument('--crash', help='crash and burn.', action='store_true')
  parser.add_argument('--server', metavar='ip address', help='server string.')
  parser.add_argument('--port', metavar='N', type=int, help='port to connect to.')
  parser.add_argument('--local',  help='run locally with no server.', action='store_true')

  argz = vars(parser.parse_args())

  # Basic options - defaults
  fps = 1
  address = "localhost"
  port = 9001
  local = False

  # Parse arguments
  if argz["fps"]:
    fps = argz["fps"]

  if argz["server"]:
    address = argz["server"]

  if argz["port"]:
    port = argz["port"] 

  if argz["local"]:
    local = True

  # game choice options
  if argz["pygame"]:

    tetris = tetris.Tetris();
    import pygame_wrapper, pygame
    wrapper = pygame_wrapper.Wrapper(tetris.buffer, tetris.boardX, tetris.boardY)
    game = Game(tetris,fps,local,address,port,wrapper)


    # Bind pygame keyboard events to tetris game logic
    wrapper.register_event( pygame.KEYDOWN, pygame.K_LEFT, tetris.goLeft )
    wrapper.register_event( pygame.KEYDOWN, pygame.K_RIGHT, tetris.goRight )
    wrapper.register_event( pygame.KEYDOWN, pygame.K_SPACE, tetris.goRotate )
    wrapper.register_event( pygame.KEYDOWN, pygame.K_DOWN, tetris.goDown )

    #game.connectToServer()
    game.loop()

  elif argz["crash"]:
    import pygame_wrapper, pygame, screensaver

    crashburn = screensaver.FileToBuffer()
    wrapper = pygame_wrapper.Wrapper(crashburn.buffer, crashburn.boardX, crashburn.boardY)
    game = Game(crashburn,fps,local,address,port,wrapper)
   
    game.loop()


  else:
    tetris = tetris.Tetris();
    game = Game(tetris,fps,local,address,port)
    game.loop()

