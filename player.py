import math

import pygame


class Player(object):
    def __init__(self, speed, game):
        self.x = 14
        self.y = 26
        self.speed = speed
        
        self.game = game
        
        self.rotation = 0
        self.movementPossible = [True, True, True, True]
        
        self.animation_step = 0
        self.animation_index = 1
        
        self.last_anim_frame = 0
        
        self.direction = (-1, 0)
        
    def update_movement_possible(self):
        pos = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        x_last_pos = math.floor(self.x) if self.direction[0] > 0 else math.ceil(self.x)
        y_last_pos = math.floor(self.y) if self.direction[1] > 0 else math.ceil(self.y)
        
        for i, direction in enumerate(pos):
            if self.game.grid[y_last_pos + direction[1]][x_last_pos + direction[0]].type == "border":
                self.movementPossible[i] = False
            else:
                self.movementPossible[i] = True
    
    def move(self, x=0, y=0):
        self.direction = (x, y)
    
        self.x += x
        self.y += y
        
        if self.x < 0:
            self.x = self.game.size[0]
        if self.x > self.game.size[0]:
            self.x = 0