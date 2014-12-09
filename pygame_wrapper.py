"""
pygame_wrapper.py - wrap around a buffer to visualise the game
author : Benjamin Blundell
email : oni@section9.co.uk

uses pygame to visualise the state

"""

import pygame
from pygame.locals import *

class Wrapper:

    ''' A pygame wrapper around a basic game state '''

    def __init__(self, game_buffer, bufferX, bufferY):
        self.running = True
        self._display_surf = None
        self.buffer = game_buffer
        self.bufferX = bufferX
        self.bufferY = bufferY
        self.block_size = 20
        self.size = self.weight, self.height = bufferX * self.block_size, bufferY * self.block_size
        self.palette = { "0" : (0,0,0), "I" : (0,255,255), "Z" : (255,0,0), "S": (0,255,0), "O" : (200,200,200), "T" : (255,0,255), "L": (255,0,255), "J" : (0,0,255)}
        self.event_checks = []

    def init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
  
        return True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        
        for check in self.event_checks:
            if check[0] == event.type:
                if check[1] == event.key:
                    check[2]()
    

    def register_event(self, event_type, subtype, func):
        self.event_checks.append( (event_type, subtype, func) )


    def on_render(self):

        self._display_surf.fill(0)

        for i in range(0,self.bufferY):
            for j in range(0,self.bufferX):
                if self.buffer[i][j] != 0:
                    rect = (j * self.block_size,  (self.bufferY - i - 1) * self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(self._display_surf, self.palette[self.buffer[i][j]], rect )

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

