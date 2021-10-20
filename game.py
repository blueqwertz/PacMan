import pygame

from player import Player
from enemy import Enemy
from render import RenderEngine

class PacMan(object):
    def __init__(self, win, x_size, y_size, tyle_size):
        self.win = win
        self.run = True
        
        self.clock = pygame.time.Clock()
        
        self.pause = False
        
        self.coins = []
        
        self.frame_rate = 60
        
        self.enemies = []
        
        self.keys_pressed = [False, False, False, False]
        
        self.size = [x_size, y_size]
        self.grid = self.load_map()
        self.block_size = tyle_size
        
        self.player_speed = 11
        self.player = Player(self.player_speed)
        
        self.renderer = RenderEngine(win, self, tyle_size, x_size, y_size)
    
    def load_map(self):
        temp = []
        with open("map.txt", "r") as f:
            map = f.read()
            map = map.split("\n")
        for row in map:
            row_temp = [Tyle("empty") for x in range(self.size[0])]
            for i, letter in enumerate(row):
                if letter == "B":
                    row_temp[i] = (Tyle("border"))
                elif letter == "C":
                    row_temp[i] = (Tyle("coin"))
                elif letter == "D":
                    row_temp[i] = (Tyle("dot"))
                elif letter == "E":
                    row_temp[i] = (Tyle("empty"))
            temp.append(row_temp)
        return temp
    
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.keys_pressed[0] = True
                if event.key == pygame.K_UP:
                    self.keys_pressed[1] = True
                if event.key == pygame.K_RIGHT:
                    self.keys_pressed[2] = True
                if event.key == pygame.K_DOWN:
                    self.keys_pressed[3] = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keys_pressed[0] = False
                if event.key == pygame.K_UP:
                    self.keys_pressed[1] = False
                if event.key == pygame.K_RIGHT:
                    self.keys_pressed[2] = False
                if event.key == pygame.K_DOWN:
                    self.keys_pressed[3] = False
    
    
    def render(self):
        self.renderer.new_screen()
        self.renderer.draw_background()
        self.renderer.draw_grid_lines()
        self.renderer.render_grid(self.grid)
        self.renderer.draw_player()
            
    def frame(self):
        delta = self.clock.get_rawtime()
        for i, key in enumerate(self.keys_pressed):
            if key:
                self.player.send_key(i, delta)
        
        self.clock.tick(self.frame_rate)
        
    
    def update(self):
        pygame.display.flip()
        

class Tyle(object):
    def __init__(self, tyle_type):
        self.colors = {"border": (0, 0, 255), "coin": (255, 0, 0), "empty": (0, 0, 0), "dot": (255, 0, 0)}
        self.type = tyle_type
        self.color = self.colors[tyle_type]