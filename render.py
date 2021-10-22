import pygame
import string

class RenderEngine(object):
    def __init__(self, win, game, block_size, x_size, y_size):
        self.win = win
        self.game = game
        self.player = game.player
        self.screen_size_x = x_size
        self.screen_size_y = y_size
        self.block_size = block_size
        
        self.SpriteLoader = SpriteLoader()
                
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
        
        if mouthOpen == 0:
            if rotation == 2:
                pacmanImage = pygame.image.load(self.ElementPath + "tile049.png")
            elif rotation == 1:
                pacmanImage = pygame.image.load(self.ElementPath + "tile052.png")
            elif rotation == 3:
                pacmanImage = pygame.image.load(self.ElementPath + "tile053.png")
            elif rotation == 0:
                pacmanImage = pygame.image.load(self.ElementPath + "tile048.png")
        elif mouthOpen == 1:
            if rotation == 2:
                pacmanImage = pygame.image.load(self.ElementPath + "tile051.png")
            elif rotation == 1:
                pacmanImage = pygame.image.load(self.ElementPath + "tile054.png")
            elif rotation == 3:
                 pacmanImage = pygame.image.load(self.ElementPath + "tile055.png")
            elif rotation == 0:
                pacmanImage = pygame.image.load(self.ElementPath + "tile050.png")
        else:
            pacmanImage = pygame.image.load(self.ElementPath + "tile112.png")
        img = pygame.transform.scale(pacmanImage, (self.block_size * 2, self.block_size * 2))
        
        self.win.blit(img, (self.player.x * self.block_size - img.get_width() / 4, self.player.y * self.block_size - img.get_height() / 4))
        
    def draw_background(self):
        self.win.blit(self.bg, (0, 0))
        pass
    
    def render_grid(self, grid):
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
        self.text("HIGH SCORE", "white", (190, 5))
        for i in range(self.game.lives):
            
            img = pygame.transform.scale(pygame.image.load(self.ElementPath + "tile052.png"), (self.block_size, self.block_size))
            self.win.blit(img, (i * img.get_width() + 20, (self.game.size[1] - 1.5) * self.block_size))
    
    def text(self, text, color:str, pos) -> None:
        text = str(text.lower())
        color = color.lower()
        
        if not color in ["white", "red", "pink", "blue", "yellow"]:
            raise NameError("color not supported")
    
        for i, letter in enumerate(text):
            if letter == " ":
                continue
            letterInd = ord(letter) - 97
            if letterInd >= 15:
                letterInd += 1
            index = "{:03d}".format(letterInd + (64 * ["white", "red", "pink", "blue", "yellow"].index(color)))
            letterImg = pygame.image.load(self.TextPath + f"tile{index}.png")
            img = pygame.transform.scale(letterImg, (self.block_size, self.block_size))
            self.win.blit(img, (pos[0] + i * img.get_width(), pos[1]))
            
        
        