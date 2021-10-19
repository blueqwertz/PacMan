import pygame
import os

from render import RenderEngine
from game import PacMan

pygame.init()

tiles_w = 28
tiles_h = 36
tile_size = 20

screen_w = tiles_w * tile_size
screen_h = tiles_h * tile_size


windowX = 100
windowY = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX,windowY)

pygame.init()
pygame.joystick.init()

win = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("PacMan")
    

def run(win):
    Game = PacMan(win)

    while Game.run:
        Game.frame()
        
        Game.update()
        
        Game.keys()

run(win)