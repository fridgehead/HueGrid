"""
message.py - read in the glyphs for a-z0-0 and write a message
author : Benjamin Blundell
email : oni@section9.co.uk

"""
from buffergame import BufferGame, loadFromFile
import math

class MessageWriter(BufferGame):

  ''' Write a message then repeat '''

  def __init__(self, boardX = 14, boardY = 13, filename="glyphs.txt", message="hack the planet", steps_second="1"):
    super(MessageWriter,self).__init__(boardX,boardY)


    self.playhead = 0
    self.currentFrame = 0
    self.message = message
    self.messagePos = 0
    self._dframes = 0
    self.scrollSpeed = steps_second

    data = loadFromFile(boardX, boardY, filename)

    self.frames = data["buffers"]
    self.timeLength = data["duration"]

    # Set first frame
    print(self.message)
    self.copyBuffer(self.frameForKey( self.message[0])["buffer"] )

  def frameForKey(self,key):
    for frame in self.frames:
      if frame["key"] == key.lower():
        return frame
    return self.frames[0] # bit naughty - corresponds to '_' in the file - good for spaces

  
  def frame(self,fps=2):
  
    self._dframes += 1
    if self._dframes >= self.scrollSpeed:
      self._dframes = 0

      self.copyBuffer(self.frameForKey(self.message[self.messagePos])["buffer"] )

      self.messagePos += 1
      if self.messagePos >= len(self.message):
        self.messagePos = 0


class MessageScroller(MessageWriter):

  ''' Scroll instead of flash message '''

  def __init__(self, boardX = 14, boardY = 13, filename="glyphs.txt", message="hack the planet", steps_second=1):
    super(MessageScroller,self).__init__(boardX,boardY,filename,message)

    self.scrollPos = 0
    self._dsteps = 0
    self.stepsPerSecond = steps_second


  def slitBuffer(self, bufferLeft, bufferRight, shift):
    if shift == 0:
      return bufferLeft

    for ridx in range(0,self.boardY):
      for cidx in range(0,self.boardX):
        if cidx + shift >= self.boardX:
          self.buffer[ridx][cidx] = bufferRight[ridx][ cidx - self.boardX + shift]
        else:
          self.buffer[ridx][cidx] = bufferLeft[ridx][cidx + shift]



  def frame(self,fps=2):

    ''' we scroll by keeping two letters at a time and moving between buffers '''
 
    dt = 1/fps
    self._dsteps += dt * float(self.stepsPerSecond)

    fd = int(math.floor(self._dsteps))

    if fd >= 1:

      for i in range(0,fd):
      
        self.slitBuffer(self.frameForKey(self.message[self.messagePos])["buffer"], 
          self.frameForKey(self.message[self.messagePos+1])["buffer"],self.scrollPos)

        self.scrollPos += 1
        if self.scrollPos >= self.boardX:
          self.messagePos += 1
          self.scrollPos = 1
        if self.messagePos + 1 >= len(self.message):
          self.messagePos = 0

      self._dsteps = 0


    
