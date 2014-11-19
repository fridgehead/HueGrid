"""
game.py - base file for the tetris game
author : Benjamin Blundell
email : oni@section9.co.uk

"""

import tetris, argparse, time, sys


class Game:

  def __init__(self, tetris, fps=2, pygame=False):
    self.fps = fps;
    self.interval = 1 / fps;
    self.tetris = tetris
    self.pygame = pygame

    if self.pygame:
      self.pygame.init()

  def loop(self):
    start_time = time.time()
    self.running = True
    
    while(self.running):
       
      # Cx pygame - kill it but keep the game running 
      if self.pygame:
        if self.pygame.running:
          self.pygame.frame()
        else:
          self.pygame.cleanup()
          self.pygame = False

      now = time.time()
      if now - start_time >= self.interval:
        print("---")
        self.tetris.frame()
        self.tetris.prettyPrint()
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
    print()
    print('You pressed Ctrl+C - Exiting Tetris')
    game.quit()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)
  print ('Launching Tetris...')
  print ('Press Ctrl+C to exit')

  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--fps', metavar='N', type=int, help='overall framerate')
  parser.add_argument('--pygame', help='launch a pygame window', action='store_true')

  argz = vars(parser.parse_args())

  tetris = tetris.Tetris();

  fps = 1

  if argz["pygame"]:

    import pygame_wrapper
    wrapper = pygame_wrapper.Tetris(tetris)
    game = Game(tetris,fps,wrapper)
    game.loop()

  else:
    game = Game(tetris,fps)
    game.loop()

