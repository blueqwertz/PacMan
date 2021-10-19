import pygame

from player import Player
from enemy import Enemy

class PacMan(object):
    def __init__(self, win):
        self.win = win
        self.run = True
        
        self.clock = pygame.time.Clock()
        
        self.pause = False
        
        self.frame_rate = 60
        
        self.enemies = []
        
        self.player_speed = 1
        self.player = Player(self.player_speed)
    
    def keys(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                self.joystick_connected = True
                self.init_joystick()
            
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joystick = None
                self.joystick_connected = False
            
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
    
    def frame(self):
        self.clock.tick(self.frame_rate)
    
    def update(self):
        pygame.display.flip()