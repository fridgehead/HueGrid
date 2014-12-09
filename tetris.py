"""
tetris.py - a simple game of tetris
author : Benjamin Blundell
email : oni@section9.co.uk


"""


import random, copy
from buffergame import BufferGame, loadFromFile

 
class Tetris(BufferGame):
  ''' Basic game logic for tetris. We deal in discrete states with no notion
  of time, more to do with frames and discrete values '''

  def __init__(self, boardX = 14, boardY = 13):
  
    super(Tetris,self).__init__(boardX,boardY) 

    self.blocks = [
        { 'bits' : [[-1,0],[ 0,0],[1,0],[2,0]], 'type' : 'I' , 'pos' : [0,0] },  # Long piece
        { 'bits' : [[-1,1],[-1,0],[0,0],[1,0]], 'type' : 'J' , 'pos' : [0,0] },  # Left L
        { 'bits' : [[ 1,1],[-1,0],[0,0],[1,0]], 'type' : 'L' , 'pos' : [0,0] },  # Right L
        { 'bits' : [[ 1,1],[ 0,0],[1,0],[0,1]], 'type' : 'O' , 'pos' : [0,0] },  # Square
        { 'bits' : [[ 0,1],[-1,0],[0,0],[1,1]], 'type' : 'Z' , 'pos' : [0,0] },  # S
        { 'bits' : [[-1,1],[ 0,1],[0,0],[1,0]], 'type' : 'S' , 'pos' : [0,0] },  # Z
        { 'bits' : [[ 0,1],[-1,0],[0,0],[1,0]], 'type' : 'T' , 'pos' : [0,0] }   # T
    ]


    self.rotClock = ((0,-1),(1,0))
    self.rotCounter = ((0,1),(-1,0))
    self.rot180 = ((-1,0),(0,-1))

    self.rotations = [self.rotCounter,self.rotClock,self.rot180]

    self.level = 1
    self.state = "READY"
    self.eventQueue = []    # list of tuples - function and arg
    self._dframes = 0       # frames passed between ticks
    self._eframes = 0       # end game animation frames passed

    # Game over data

    gameover_data = loadFromFile(boardX, boardY, "game_over.txt")

    self._gameOverFrames = gameover_data["buffers"]
    self._gameOverDuration = gameover_data["duration"]

    # start data
    start_data = loadFromFile(boardX, boardY, "start_game.txt")
    self._startFrames = start_data["buffers"]
    self._startDuration = start_data["duration"]

  def start(self):
    ''' Clear the board and start the game '''
    self.clearBuffer()

    self.level = 1
    self.currentBlock = self.createBlock()
    self.moveHere(self.currentBlock,(0,-1))

    self.state = "PLAYING"

  def rotate(self, matrix, block):
    ''' rotate the current block returning a new block - non destructive '''
    new_block = copy.deepcopy(block)

    # Ignore the square 'O'
    if block['type'] != 'O':
      for bit in new_block['bits']:
        x = bit[0] # todo - presumably a copy here?
        y = bit[1]
        bit[0] = x * matrix[0][0] + y * matrix[1][0]
        bit[1] = x * matrix[0][1] + y * matrix[1][1]

    return new_block
              

  def createBlock(self):
    ''' create a new block at the top of the screen '''
    # Pick random block
    c =  random.randint(0,len(self.blocks)-1)
    new_block = self.blocks[c : c + 1 ][0]

    if new_block['type'] != 'O':
      c = random.randint(0,len(self.rotations))
      if c != len(self.rotations):
        # Garbage collect here as we loose new_block and gain another
        new_block = self.rotate(self.rotations[c],new_block)
    
    # Find highest y point - if we rotate of course
    topy = 0
    for [x,y] in new_block['bits']:
      if y > topy:
        topy = y

    new_block['pos'][0] = self.boardX / 2
    new_block['pos'][1] = self.boardY - topy

 
    return new_block

    ''' Events can occur at any time so they sort
    of ruin the discrete nature of state changes really so we queue
    them '''

  def _move(self,offset):
    self.moveIfPoss(self.currentBlock,offset)

  def goLeft(self):
    self.eventQueue.append( (self._move,(-1,0)))

  def goRight(self):
    self.eventQueue.append( (self._move,(1,0)))
  
  def goDown(self):
    self.eventQueue.append( (self._move,(0,-1)))

  def goStart(self):
    if self.state == "READY":
      self.eventQueue = [] # clear so we don't roll over into rotate or something
      self._eframes = 0 # reset the eframes ready for game over
      self.start()

  def _rotate(self,clockwise):
    ''' Rotate a block - somewhat more involved '''
    tblock = self.rotate(self.rotClock, self.currentBlock)
    if not clockwise:
   		tblock = self.rotate(self.rotCounter, self.currentBlock)
    if self.canMoveHere(tblock, (0,0)):
      # garbage collect
      self.clearBlock(self.currentBlock)
      self.currentBlock = tblock
      self.moveHere(self.currentBlock, (0,0))


  def goRotate(self):
    self.eventQueue.append( (self._rotate, True))


  def canMoveHere(self, block, offset):
    ''' check if we can move into the new location specified by offset '''
    for [x,y] in block['bits']:

      xp = x + block['pos'][0] + offset[0]
      yp = y + block['pos'][1] + offset[1]

      if xp < 0 or xp >= self.boardX:
        return False

      if yp < 0 or yp >= self.boardY:
        return False

      if self.buffer[yp][xp] != 0 :
        # Cx its not moving into itself
        xp = x + offset[0]
        yp = y + offset[1]

        if not [xp,yp] in block['bits']:
          return False

    return True

  def moveIfPoss(self,block,offset):
    ''' convinience function '''
    if self.canMoveHere(block,offset):
      self.moveHere(block,offset)
      return True
    return False

  def clearBlock(self,block):
    ''' clear a block from the buffer '''
    for [x,y] in block['bits']:

      xp = x + block['pos'][0]
      yp = y + block['pos'][1]

      if xp >= 0 and xp < self.boardX and yp >= 0 and yp < self.boardY:
        self.buffer[yp][xp] = 0

  def moveHere(self, block, offset):
    ''' clear where the block currently is and move it offset amount and set '''
    # Clear buffer
    self.clearBlock(block)

    for [x,y] in block['bits']:

      xp = x + block['pos'][0] + offset[0]
      yp = y + block['pos'][1] + offset[1]
   
      self.buffer[yp][xp] = block['type']

    block['pos'][0] += offset[0]
    block['pos'][1] += offset[1]
    

  def check_lines(self):
    ''' Check to see if we've completed any lines '''
    lines = []
    for i in range(0,self.boardY):
      complete = True
      for j in range(0,self.boardX):
        if self.buffer[i][j] == 0:
          complete = False
          break
      if complete:
        lines.append(i)

    # Should be in order from the bottom up

    for lidx in range(0,len(lines)):

      line = lines[lidx] - lidx

      for i in range(line,self.boardY):
        if i != self.boardY - 1:
        	for j in range(0,self.boardX):
         		self.buffer[i][j] = self.buffer[i+1][j] 
        else:
        	for j in range(0,self.boardX):
						self.buffer[i][j] = 0


  def check_events(self):
    ''' Go through the events popping them '''
    while len(self.eventQueue) > 0:
      event = self.eventQueue.pop()
      event[0](event[1])


  def tick(self):
    ''' update the state of the game by one tick
    this is a logic tick but since we have a low fps its almost 
    analogous to a game loop with no dt '''

    self.check_lines()
    
    if self.canMoveHere(self.currentBlock, (0,-1)):
      self.moveHere(self.currentBlock,(0,-1))
    else:
      # Try and add another
      self.currentBlock = self.createBlock()
  
      if not self.canMoveHere( self.currentBlock, (0,-1) ):
      	self.state = "GAME_OVER"
      else:
        # garbage collect
        self.moveHere(self.currentBlock,(0,-1))

  def game_over(self,fps=2):
    ''' Game over animation '''
    
    dd = float(self._eframes) / float(fps)

    if dd >= self._gameOverDuration: # 3 second game over screen
      self._eframes = 0
      self.clearBuffer()
      self.state = "READY"
      return
    else:
      # draw the game over screen - find out which frame we want
      self.clearBuffer()
      dt = 0
  
      for frame in self._gameOverFrames:
        dt += frame["time"]
        if dd <= dt:
          self.copyBuffer(frame["buffer"])
          break

    self._eframes += 1

  def ready(self,fps=2):
    ''' display a simple tetris anination and press space to play. Pretty
    much the same as game over I figure '''
    self.clearBuffer()
    dt = 0
    dd = float(self._eframes) / float(fps)

    if dd >= self._startDuration:
      self._eframes = 0
      self.clearBuffer()
      self.copyBuffer(self._startFrames[0]["buffer"])

    for frame in self._startFrames:
      dt += frame["time"]
      if dd <= dt:
        self.copyBuffer(frame["buffer"])
        break

    self._eframes += 1



  def frame(self,fps=2):
    ''' We've had another frame. What should we do next?
	  We take an optional fps to get some idea of how fast
	  we are going for things like game start, block fall
	  button press etc '''

    if self.state == "GAME_OVER":
      self.game_over(fps)

    elif self.state == "PLAYING":

      self.check_events()

      # self.tick is called depending on the level / difficulty of the game
      # For now we just use a basis of 1 second drops
      self._dframes += 1
      if self._dframes / fps >= 1: # 1 second - 1 level
        self.tick()
        self._dframes = 0

    elif self.state == "READY":
      self.ready(fps)


if __name__ == "__main__" : 
  tetris = Tetris()
    