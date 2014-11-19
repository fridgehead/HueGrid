"""
pygame_wrapper.py - wrap around tetris to visualise the game
author : Benjamin Blundell
email : oni@section9.co.uk

uses pygame to visualise the state

"""




import pygame
from pygame.locals import *

class Tetris:

    ''' A pygame wrapper around the tetris game state '''

    def __init__(self, tetris):
        self.running = True
        self._display_surf = None
        self.tetris = tetris
        self.block_size = 20
        self.size = self.weight, self.height = self.tetris.boardX * self.block_size, self.tetris.boardY * self.block_size
        self.palette = { "I" : (0,255,255), "Z" : (255,0,0), "S": (0,255,0), "O" : (200,200,200), "T" : (255,0,255), "L": (255,0,255), "J" : (0,0,255)}


    def init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.tetris.start()
        self.clock = pygame.time.Clock()
        self.tickTimer = 0

        return True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        
        # Keys for playing the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.tetris.goLeft()
            if event.key == pygame.K_RIGHT:
                self.tetris.goRight()
            if event.key == pygame.K_SPACE:
                self.tetris.goRotate()
            if event.key == pygame.K_DOWN:
                self.tetris.goDown()

    '''
    def on_loop(self):
        # Call the tick for the tetris game
        msElapsed = self.clock.tick(30)
        self.tickTimer += msElapsed / 1000.0
    
        if (self.tickTimer > 1.0): # TODO - depending on level
            self.tickTimer = 0
            self.tetris.tick()
    '''

    def on_render(self):

        self._display_surf.fill(0)

        for i in range(0,self.tetris.boardY):
            for j in range(0,self.tetris.boardX):
                if self.tetris.buffer[i][j] != 0:
                    rect = (j * self.block_size,  (self.tetris.boardY - i - 1) * self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(self._display_surf, self.palette[self.tetris.buffer[i][j]], rect )

        pygame.display.update()

    def cleanup(self):
        pygame.quit()
 

    def frame(self):
        for event in pygame.event.get():
            self.on_event(event)
            #self.on_loop()
        self.on_render()

    def on_execute(self):
        if self.init() == False:
            self._running = False
 
        while( self._running ):
            self.frame()
  
        self.cleanup()

