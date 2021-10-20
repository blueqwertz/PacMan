import pygame
class RenderEngine(object):
    def __init__(self, win, game, block_size, x_size, y_size):
        self.win = win
        self.game = game
        self.player = game.player
        self.screen_size_x = x_size
        self.screen_size_y = y_size
        self.block_size = block_size
        
        self.sprites = [pygame.image.load("img/0.png"), pygame.image.load("img/1.png"), pygame.image.load("img/2.png"), pygame.image.load("img/3.png")]
        
        self.bg = pygame.transform.scale(pygame.image.load("bg.png"), (self.screen_size_x * self.block_size, self.screen_size_y * self.block_size))
        
    def new_screen(self):
        self.win.fill((0, 0, 0))
        
    def draw_grid_lines(self):
        for i in range(self.screen_size_x):
            pygame.draw.line(self.win, (128, 128, 128), (i * self.block_size, 0), (i * self.block_size, self.block_size * self.screen_size_y))
        for j in range(self.screen_size_y):
            pygame.draw.line(self.win, (128, 128, 128), (0, j * self.block_size), (self.block_size * self.screen_size_x, j * self.block_size))
    
    def draw_player(self):
        img = self.sprites[self.player.rotation]
        img = pygame.transform.scale(img, (self.block_size * 2, self.block_size * 2))
        
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
                    pygame.draw.circle(self.win, tyle.color, (j * self.block_size + self.block_size // 2, i * self.block_size + self.block_size // 2), self.block_size // 8)
                elif tyle.type == "dot":
                    pygame.draw.circle(self.win, tyle.color, (j * self.block_size + self.block_size // 2, i * self.block_size + self.block_size // 2), self.block_size // 4)