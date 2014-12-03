"""
message.py - read in the glyphs for a-z0-0 and write a message
author : Benjamin Blundell
email : oni@section9.co.uk

"""
from buffergame import BufferGame, loadFromFile


class MessageWriter(BufferGame):

  ''' Write a message then repeat '''

  def __init__(self, boardX = 14, boardY = 13, filename="glyphs.txt", message="hack the planet"):
    super(MessageWriter,self).__init__(boardX,boardY)


    self.playhead = 0
    self.currentFrame = 0
    self.message = message
    self.messagePos = 0

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
 
    self.copyBuffer(self.frameForKey(self.message[self.messagePos])["buffer"] )

    self.messagePos += 1
    if self.messagePos >= len(self.message):
      self.messagePos = 0

