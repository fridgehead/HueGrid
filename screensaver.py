"""
screensaver.py - some interesting effects
author : Benjamin Blundell
email : oni@section9.co.uk

"""
from buffergame import BufferGame

class FileToBuffer(BufferGame):
  ''' A basic bit of text '''

  def __init__(self, boardX = 13, boardY = 14, filename="crashburn.txt"):
     
    super(FileToBuffer,self).__init__(boardX,boardY)

    self.frames = []
    self.playhead = 0
    self.timeLength = 0
    self.currentFrame = 0

    with open(filename) as f:
    
      ridx = boardY -1
      try:
        for line in f.readlines():

          if "time" in line:
            # Create a new frame
            new_frame = { "game_buffer" :[], "time" : 0  }
            new_frame["time"] = float(line.split(" ")[1])
            self.timeLength += new_frame["time"]


            for i in range(0,self.boardY):
              row = []   
              for j in range(0,self.boardX):
                row.append( 0 )
              new_frame["game_buffer"].append(row)
              
            self.frames.append( new_frame )
            ridx = boardY -1

          else:
            
            cidx = 0
            for char in line:
              if char != '\n':
                self.frames[len(self.frames)-1]["game_buffer"][ridx][cidx] = char
                cidx+=1

            ridx-=1

        # Set first frame
        self.copyFrame(0)

      except:
        print("Failed to read frame format.")


  def copyFrame(self, idx):
    ''' Copy a frame into the actual buffer '''
    for i in range(0,self.boardY):
      for j in range(0,self.boardX):
        self.buffer[i][j] = self.frames[idx]["game_buffer"][i][j]
    self.currentFrame = idx
    
  
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
          self.copyFrame(idx)
          break

      idx+=1

    #print(idx,self.timeLength,self.playhead)

 

