import pygame
import time
from os import system, name, environ
from pygame import sprite

from pygame.sprite import Sprite

if name == 'nt':
        _ = system('cls')
else:
    _ = system('clear')

from scripts.game import PacMan
from scripts.sprite_loader import SpriteLoader

pygame.init()

tile_size = 20

screen_w = 28 * tile_size
screen_h = 36 * tile_size


windowX = 0
windowY = 30
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX,windowY)

pygame.init()
pygame.joystick.init()

win = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("PacMan")

def run(win):
    Game = PacMan(win, tyle_size=20)
    Game.homescreen()
    try:
        while Game.run:
            Game.frame()
            Game.render()
            Game.update()
            Game.keys()
    except KeyboardInterrupt:
        print("byebye")

run(win)