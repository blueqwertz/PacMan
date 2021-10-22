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
        
        self.score = 0
        
        self.time_last_move = 0
        self.frame_rate = 60
        

        self.animation_steps = 4
        
        self.enemies = []
        
        self.size = [x_size, y_size]
        
        self.grid = self.load_map()
        
        self.block_size = tyle_size
        
        self.showDot = True
        self.showDotCount = 0
        self.showDotDelay = 20
        
        self.lives = 3
        
        self.player_speed = 11
        self.ghosts_frightened = False

        self.player = Player(self)
        
        self.renderer = RenderEngine(win, self, tyle_size, x_size, y_size)
    
    def frame(self):
        delta = self.clock.get_rawtime() / 1000
                
        self.time_last_move += delta
        
        self.showDotCount += 1
        
        if self.showDotCount >= self.showDotDelay:
            self.showDotCount = 0
            self.showDot = not self.showDot
        if self.time_last_move >= (1 / self.player_speed) * self.player.speed:
            self.player.move()
            self.time_last_move %= (1 / self.player_speed) * self.player.speed
        
        self.player.update_anim()
        self.check_coin_collide()
        
        self.clock.tick(self.frame_rate)
    
    def init_joystick(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
    
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
                return
            
            if event.type == pygame.KEYDOWN:
                movementKeys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

                for i, key in enumerate(movementKeys):
                    if event.key == key:
                        self.player.new_dir = i
    
    def check_coin_collide(self):
        pos = (self.player.x, self.player.y)
        try:
            if round(pos[0]) == pos[0] and round(pos[1]) == pos[1]:
                if self.grid[int(pos[1])][int(pos[0])].type == "coin":
                    self.grid[int(pos[1])][int(pos[0])] = Tyle("empty")
                    self.score += 10
                
                if self.grid[int(pos[1])][int(pos[0])].type == "dot":
                    self.grid[int(pos[1])][int(pos[0])] = Tyle("empty")
                    self.ghosts_frightened = True
        except:
            pass
    
    def removeAllKeyPressed(self):
        for i in range(len(self.keys_pressed)):
            self.keys_pressed[i] = False
    
    def render(self):
        self.renderer.new_screen()
        self.renderer.draw_background()
        self.renderer.render_grid(self.grid)
        self.renderer.draw_player()
        self.renderer.draw_grame_info()      
    
    def update(self):
        pygame.display.flip()
        

class Tyle(object):
    def __init__(self, tyle_type):
        self.colors = {"border": (0, 0, 255), "coin": (242, 168, 132), "empty": (0, 0, 0), "dot": (242, 168, 132)}
        self.type = tyle_type
        self.color = self.colors[tyle_type]