import pygame

class RenderEngine(object):
    def __init__(self, win, game):
        self.win = win
        self.game = game
        
    def new_screen(self):
        pygame.screen.fill((0, 0, 0))