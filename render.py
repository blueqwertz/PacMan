import pygame
from pygame.sprite import Sprite
from sprite_loader import SpriteLoader

class RenderEngine(object):
    def __init__(self, win, game, block_size, size):
        self.win = win
        self.game = game
        self.player = game.player
        self.screen_size_x, self.screen_size_y = size
        self.block_size = block_size
        
        self.SpriteLoader = SpriteLoader()
        
        self.bg = pygame.transform.scale(pygame.image.load("bg.png"), (self.screen_size_x * self.block_size, self.screen_size_y * self.block_size))
        
    def new_screen(self):
        self.win.fill((0, 0, 0))
        
    def draw_grid_lines(self):
        for i in range(self.screen_size_x):
            pygame.draw.line(self.win, (128, 128, 128), (i * self.block_size, 0), (i * self.block_size, self.block_size * self.screen_size_y))
        for j in range(self.screen_size_y):
            pygame.draw.line(self.win, (128, 128, 128), (0, j * self.block_size), (self.block_size * self.screen_size_x, j * self.block_size))
    
    def draw_player(self):
        mouthOpen = self.player.mouthOpen
        rotation = self.player.direction
        
        img = pygame.transform.scale(self.SpriteLoader.load("PacMan", Rotation=rotation, AnimCount=mouthOpen, PlayerDead=self.player.dead, PlayerDeadAnim=self.player.deadAnim), (self.block_size * 2, self.block_size * 2))
        
        self.win.blit(img, (self.player.x * self.block_size - img.get_width() / 4, self.player.y * self.block_size - img.get_height() / 4))
        
    def draw_background(self):
        self.win.blit(self.bg, (0, 0))
        pass
    
    def draw_grid(self, grid):
        for i, row in enumerate(grid):
            for j, tyle in enumerate(row):
                if tyle.type == None:
                    continue
                if tyle.type == "coin":
                    pygame.draw.circle(self.win, tyle.color, (j * self.block_size + self.block_size // 2, i * self.block_size + self.block_size // 2), self.block_size // 5)
                elif tyle.type == "dot":
                    if not self.game.showDot:
                        continue
                    pygame.draw.circle(self.win, tyle.color, (j * self.block_size + self.block_size // 2, i * self.block_size + self.block_size // 2), self.block_size // 2)
    
    def draw_grame_info(self):
        self.text("HIGH SCORE", (190, 0))
        self.text(self.game.score, (80, 21))
        self.text(self.game.highscore, (270, 21))
        for i in range(self.game.lives):
            
            img = pygame.transform.scale(self.SpriteLoader.load("PacMan", 1, 1), (self.block_size, self.block_size))
            self.win.blit(img, (i * img.get_width() + 20, (self.game.size[1] - 1.5) * self.block_size))
    
    def draw_ghosts(self):
        for ghost in self.game.enemies:
            # pygame.draw.line(self.win, (255, 255, 255), (ghost.x * self.block_size, ghost.y * self.block_size), (ghost.target[0] * self.block_size, ghost.target[1] * self.block_size))
            img = pygame.transform.scale(self.SpriteLoader.load("Ghost", ghost=ghost), (self.block_size * 2, self.block_size * 2))
            self.win.blit(img, (ghost.x * self.block_size - img.get_width() / 4, ghost.y * self.block_size - img.get_height() / 4))
    
    def text(self, text, pos):
        text = str(text).lower()
            
        # if not color in ["white", "red", "pink", "blue", "yellow"]:
        #     raise NameError("color not supported")
        curX = pos[0]
        for i, letter in enumerate(text):
            if letter == " ":
                curX += (curX - pos[0]) / (i)
                continue
            letterInd = ord(letter) - 97
            if letterInd >= 15:
                letterInd += 1
            img = pygame.transform.scale(self.SpriteLoader.load("Letter", letter=letter), (19, 19))
            self.win.blit(img, (curX, pos[1]))
            curX += img.get_width() + 3
            
        
        