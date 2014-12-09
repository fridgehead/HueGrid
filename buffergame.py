"""
buffergame.py - the base class for all the games
author : Benjamin Blundell
email : oni@section9.co.uk

"""


def loadFromFile(boardX, boardY, filename):
  ''' function that loads buffers from a file using our format.
      file format is: 
      
      time <seconds>
      <bufferdata>
      ...

      return data is {
        "buffers" : [
          "time" : <seconds> OR "key" : <key>
          "buffer": <data>
        ]
        "duration" : <seconds>
      }

  '''
  
  buffers = []
  timeLength = 0

  def _newBuffer():
    for i in range(0,boardY):
      row = []
      for j in range(0,boardX):
        row.append( 0 )
      new_frame["buffer"].append(row)
            
    buffers.append( new_frame )


  with open(filename) as f:
  
    ridx = boardY - 1
    try:
      for line in f.readlines():

        if "time" in line:
          # Create a new frame
          new_frame = { "buffer" :[], "time" : 0  }
          new_frame["time"] = float(line.split(" ")[1])
          timeLength += new_frame["time"]

          _newBuffer()
          ridx = boardY - 1

        elif "key" in line:
        # create a new frame with a special key and a default time
          new_frame = { "buffer" :[], "key" : "a"  }
          new_frame["key"] = line.split(" ")[1].strip()
      
          _newBuffer()
          ridx = boardY - 1          

        else:

          if ridx >= 0: 
          
            cidx = 0
            for char in line:
              if char != '\n':
                buffers[len(buffers)-1]["buffer"][ridx][cidx] = char
                cidx+=1

          ridx-=1
    except:
      print("Failed to read frame format.")
      raise

  return { "buffers" : buffers, "duration" : timeLength }



class BufferGame(object):

  ''' Base class that creates and sets buffers '''

  def __init__(self, boardX = 14, boardY = 13):

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

  def clearBuffer(self):
    for i in range(0,self.boardY):
      for j in range(0,self.boardX):
        self.buffer[i][j] = 0

  # A lot of the functions below are similar - maybe refactor?

  def copyBuffer(self, bbuffer):
    ''' Copy a frame into the actual buffer '''
    for i in range(0,self.boardY):
      for j in range(0,self.boardX):
        self.buffer[i][j] = bbuffer[i][j]

  def copyLinearBuffer(self, bbuffer):
    ''' Copy a linear buffer into the actual buffer '''
    idx = 0
    for i in range(0,self.boardY):
      for j in range(0,self.boardX):
        self.buffer[i][j] = bbuffer[idx]
        idx += 1

  def copyLinearBufferReversed(self, bbuffer):
    ''' Copy a linear buffer into the actual buffer reversed columns '''
    idx = 0
    for i in reversed(range(0,self.boardY)):
      for j in range(0,self.boardX):
        self.buffer[i][j] = bbuffer[idx]
        idx += 1
    

  def getLinearBuffer(self):
    data = []
    for i in range(0,self.boardY): 
      for j in range(0,self.boardX):
        data.append(self.buffer[i][j])
    
    return data

  def getLinearBufferReversed(self):
    data = []
    for i in reversed(range(0,self.boardY)):
      for j in range(0,self.boardX):
        data.append(self.buffer[i][j])

    return data

  def prettyPrint(self):
      ''' rprint the buffer out nicely '''
      for i in reversed(range(0,self.boardY)):
          for j in range(0,self.boardX):
              print(str(self.buffer[i][j])),
          print("")
      print("")