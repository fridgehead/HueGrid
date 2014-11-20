"""
game.py - base file for the tetris game
author : Benjamin Blundell
email : oni@section9.co.uk

"""

import tetris, argparse, time, sys, socket


# TODO - We need to be careful with the controls - the player cant really exceed the fps
# so we may have to actually queue events and potentially dispose of them :S More testing needed
# I suspect.

class Game:

  def __init__(self, game, fps=2, server_address="192.168.1.1", port=9001, pygame=False):
    self.fps = fps;
    self.interval = 1 / fps;
    self.game = game
    self.pygame = pygame
    self.server_address = server_address
    self.port = port

    if self.pygame:
      self.pygame.init()


  def connectToServer(self):
    ''' connect to server via udp '''
    print("LocalName: " + socket.gethostname())
    print("Connecting To: " + self.server_address + " on " + repr(self.port) )
    
    socket.create_connection((self.server_address,self.port))


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
        print("---")
        self.game.frame(dt)
        self.game.prettyPrint()
        start_time = now

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
  parser.add_argument('--fps', metavar='N', type=float, help='overall framerate')
  parser.add_argument('--pygame', help='launch a pygame window', action='store_true')
  parser.add_argument('--crash', help='crash and burn', action='store_true')

  argz = vars(parser.parse_args())

  # Basic options
  fps = 1
  address = "localhost"
  port = 9001

  if argz["fps"]:
    fps = argz["fps"]


  # game choice options
  if argz["pygame"]:

    tetris = tetris.Tetris();
    import pygame_wrapper, pygame
    wrapper = pygame_wrapper.Wrapper(tetris.buffer, tetris.boardX, tetris.boardY)
    game = Game(tetris,fps,address,port,wrapper)

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
    game = Game(crashburn,fps,address,port,wrapper)
   
    game.loop()


  else:
    tetris = tetris.Tetris();
    game = Game(tetris,fps,address,port)
    game.loop()

