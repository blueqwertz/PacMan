import math

import pygame


class Player(object):
    def __init__(self, game):
        self.x = 14
        self.y = 26
        self.speed = 1/4
        
        self.__game = game
        
        self.dead = False
        
        self.mouthOpen = 0
        self.__mouthChangeDelay = 2
        self.__mouthChangeCount = 0
        self.__mouthOpenDir = True
        
        self.direction = 0 # Left, Right, Up, Down
        self.new_dir = 0
        
        self.deadAnim = 0
        self.__deadAnimCount = 0
        self.__deadAnimDelay = 10
    
    def new_game(self):
        print("new game")
        self.x = 14
        self.y = 26
        
        self.dead = False
        
        self.mouthOpen = 0
        self.deadAnim = 0
        
        self.direction = 0 # Left, Right, Up, Down
        self.new_dir = 0
        
    
    
    def canMove(self, row, col):
        if col == -1 or col >= self.__game.size[0]:
            return True
        if self.__game.grid[int(row)][int(col)].type == "border":
            return False
        return True
    
    def update_anim(self):
        if self.dead:
            self.__deadAnimCount += 1
            if self.__deadAnimCount >= self.__deadAnimDelay:
                self.__deadAnimCount = 0
                self.deadAnim += 1
            return
        self.__mouthChangeCount += 1
        if self.__mouthChangeCount >= self.__mouthChangeDelay:
            self.__mouthChangeCount = 0
            if self.__mouthOpenDir:
                self.mouthOpen += 1
            else:
                self.mouthOpen -= 1
            
            if self.mouthOpen <= 0 or self.mouthOpen >= 3:
                self.__mouthOpenDir = not self.__mouthOpenDir
    
    def move(self):
             
        if self.x < 0:
            self.x = self.__game.size[0]
        if self.x > self.__game.size[0]:
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
            # else:
            #     print((14 - self.x) / (pygame.time.get_ticks() / 1000))
            #     print(pygame.time.get_ticks() / 1000)
                
            #     self.game.run = False