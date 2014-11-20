"""
buffergame.py - the base class for all the games
author : Benjamin Blundell
email : oni@section9.co.uk

"""



class BufferGame(object):

  ''' Base class that creates and sets buffers '''

  def __init__(self, boardX = 13, boardY = 14):

    self.boardX = boardX
    self.boardY = boardY
    self.buffer = []

    for i in range(0,self.boardY):
      row = []   
      for j in range(0,self.boardX):
        row.append( 0 )
      self.buffer.append(row)

  def frame(self,dt):
    pass

  def prettyPrint(self):
      ''' rprint the buffer out nicely '''
      for i in reversed(range(0,self.boardY)):
          for j in range(0,self.boardX):
              print(str(self.buffer[i][j])),
          print("")
      print("")