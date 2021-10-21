import math

import pygame
from pygame.constants import GL_FRAMEBUFFER_SRGB_CAPABLE


class Player(object):
    def __init__(self, game):
        self.x = 14
        self.y = 26
        self.speed = 0.25
        
        self.game = game
        
        self.mouthOpen = True
        self.mouthChangeDelay = 2
        self.mouthChangeCount = 0
                
        self.animation_step = 0
        self.animation_index = 1
        
        self.last_anim_frame = 0
        
        self.direction = 0 # Left, Right, Up, Down
        self.new_dir = 0
        
    def canMove(self, row, col):
        if col == -1 or col >= self.game.size[0]:
            return True
        if self.game.grid[int(row)][int(col)].type == "border":
            return False
        return True
    
    def move(self):
        
        if self.mouthChangeCount >= self.mouthChangeDelay:
            self.mouthChangeCount = 0
            self.mouthOpen = not self.mouthOpen
        
        self.mouthChangeCount += 1
             
        if self.x < 0:
            self.x = self.game.size[0]
        if self.x > self.game.size[0]:
            self.x = 0
        
        if self.new_dir == 2:
            if self.canMove(math.floor(self.y - self.speed), self.x) and self.x % 1.0 == 0:
                self.y -= self.speed
                self.direction = self.new_dir
                return
        elif self.new_dir == 1:
            if self.canMove(self.y, math.ceil(self.x + self.speed)) and self.y % 1.0 == 0:
                self.x += self.speed
                self.direction = self.new_dir
                return
        elif self.new_dir == 3:
            if self.canMove(math.ceil(self.y + self.speed), self.x) and self.x % 1.0 == 0:
                self.y += self.speed
                self.direction = self.new_dir
                return
        elif self.new_dir == 0:
            if self.canMove(self.y, math.floor(self.x - self.speed)) and self.y % 1.0 == 0:
                self.x -= self.speed
                self.direction = self.new_dir
                return
        
        
        if self.direction == 2:
            if self.canMove(math.floor(self.y - self.speed), self.x) and self.x % 1.0 == 0:
                self.y -= self.speed
        elif self.direction == 1:
            if self.canMove(self.y, math.ceil(self.x + self.speed)) and self.y % 1.0 == 0:
                self.x += self.speed
        elif self.direction == 3:
            if self.canMove(math.ceil(self.y + self.speed), self.x) and self.x % 1.0 == 0:
                self.y += self.speed
        elif self.direction == 0:
            if self.canMove(self.y, math.floor(self.x - self.speed)) and self.y % 1.0 == 0:
                self.x -= self.speed