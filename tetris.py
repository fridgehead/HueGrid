"""
tetris.py - a simple game of tetris
author : Benjamin Blundell
email : oni@section9.co.uk


"""


import random, copy

 
class Tetris:
    ''' Basic game logic for tetris '''

    def __init__(self):
        self.boardX = 13 # Minimum 4
        self.boardY = 14
        self.buffer = []

        for i in range(0,self.boardY):
            row = []   
            for j in range(0,self.boardX):
                row.append( 0 )

            self.buffer.append(row)

        self.blocks = [
            { 'bits' : [[-1,0],[ 0,0],[1,0],[2,0]], 'type' : 'I' , 'pos' : [0,0] },    # Long piece
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

    def start(self):
        ''' Clear the board and start the game '''
        for i in range(0,self.boardY):
            for j in range(0,self.boardX):
                self.buffer[i][j] = 0

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
        for (x,y) in new_block['bits']:
            if y > topy:
                topy = y

        new_block['pos'][0] = (self.boardX / 2)
        new_block['pos'][1] = (self.boardY - topy)
     
        return new_block


    def _move(self,offset):
        ''' internal checking func '''
        if self.state == "PLAYING":
            self.moveIfPoss(self.currentBlock,offset)

    def goLeft(self):
        self._move((-1,0))

    def goRight(self):
       self._move((1,0))
  
    def goDown(self):
       self._move((0,-1))

    def goRotate(self):
        ''' Rotate a block - somewhat more involved '''
        if self.state == "PLAYING":
            tblock = self.rotate(self.rotClock, self.currentBlock)
            if self.canMoveHere(tblock, (0,0)):
                # garbage collect
                self.clearBlock(self.currentBlock)
                self.currentBlock = tblock
                self.moveHere(self.currentBlock, (0,0))


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

            if xp >= 0 and xp <= self.boardX and yp >= 0 and yp <= self.boardX:
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
        #self.prettyPrint()

    def tick(self):
        ''' update the state of the game by one tick'''

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

    def game_over(self):
        ''' Game over animation '''
        pass


    def frame(self):
        ''' Runs as fast as possible really. Not limited in anyway '''


        if self.state == "GAME_OVER":
            pass
        
        elif self.state == "PLAYING":
            self.tick()

        elif self.state == "READY":
            self.start()


    def prettyPrint(self):
        ''' rprint the buffer out nicely '''
        for i in reversed(range(0,self.boardY)):
            for j in range(0,self.boardX):
                print(str(self.buffer[i][j])),
            print("")
        print("")


 
if __name__ == "__main__" :
   
    tetris = Tetris()
    