"""
screensaver.py - some interesting effects
author : Benjamin Blundell
email : oni@section9.co.uk

"""
from buffergame import BufferGame, loadFromFile

class FileToBuffer(BufferGame):
  ''' A basic bit of text '''

  def __init__(self, boardX = 14, boardY = 13, filename="crashburn.txt"):
     
    super(FileToBuffer,self).__init__(boardX,boardY)

    self.playhead = 0
    self.currentFrame = 0

    data = loadFromFile(boardX, boardY, filename)

    self.frames = data["buffers"]
    self.timeLength = data["duration"]

    # Set first frame
    self.copyBuffer(self.frames[0]["buffer"])

  
  def frame(self,dt):
    self.playhead += dt
    if self.playhead >= self.timeLength :
      self.playhead = 0 # loop back to the beginning

    tt = 0
    idx = 0
    for frame in self.frames:
      tt += frame["time"]
      if tt > self.playhead:
        if idx != self.currentFrame:
          self.copyBuffer(self.frames[idx]["buffer"])
          self.currentFrame = idx    
          break

      idx+=1

 

