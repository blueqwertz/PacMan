import pygame

from scripts.player import Player
from scripts.ghost import Ghost
from scripts.render import RenderEngine

class PacMan(object):
    def __init__(self, win, tyle_size, lives=3, score=0):
        self.win = win
        self.run = True
        
        self.clock = pygame.time.Clock()
            
        self.score = score
        self.highscore = int(open("highscore.txt", "r").read())
                
        self.time_last_move = 0
        self.time_last_ghost_move = 0
        self.frame_rate = 60
        
        self.dot_full = 0
        self.dot_catched = 0

        self.animation_steps = 4
        
        self.size = [28, 36]
        
        self.grid = self.load_map()
        
        self.block_size = tyle_size
        
        self.showDot = True
        self.showDotCount = 0
        self.showDotDelay = 20
        
        self.pause = False
        
        self.lives = lives

        self.ghost_mode = 0
        self.ghost_mode_time = [[0, 0], [7, 2], [27, 0], [34, 2], [54, 0], [59, 2], [64, 0]]
        self.frightened_mode_frames = 0
        self.ghost_eat_points = 200

        self.wait_frames = 0

        self.start_tick = 0
        self.total_frames = 0
        self.player_speed = 8
        self.ghost_speed = 8
        
        self.player = Player(self)
        self.player_dead = False
        self.enemies = [Ghost(x, self) for x in range(4)]
        
        self.renderer = RenderEngine(win, self, tyle_size, self.size)
    
    def homescreen(self):
        run = True
        highscore = int(open("highscore.txt", "r").read())
        title = self.renderer.SpriteLoader.TitleImg
        try:
            while run:
                title = pygame.transform.scale(title, (int(self.size[0] * self.block_size - 150), int((self.size[0] * self.block_size - 150) / title.get_width() * title.get_height())))
                self.win.blit(title, (self.size[0] * self.block_size / 2 - title.get_width() / 2, 200))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        run = False
                    
                self.clock.tick(self.frame_rate)
                pygame.display.flip()
                
        except KeyboardInterrupt:
            self.run = False
            print("byebye")
    
    def store_highscore(self):
        if self.score > self.highscore:
            open("highscore.txt", "w").write(str(self.score))
    
    def frame(self):
        if self.wait_frames > 0:
            self.wait_frames -= 1
            self.clock.tick(self.frame_rate)
            return
        
        if self.player_dead:
            self.enemies = []
            self.player.update_anim()
            self.player.dead = True
            if self.player.deadAnim >= 11:
                self.renderer.draw_player()
                pygame.time.delay(500)
                if self.lives <= 0:
                    self.run = False
                    self.store_highscore()
                    return
                self.__init__(self.win, self.block_size, lives=self.lives, score=self.score)
        
        if self.pause:
            self.clock.tick(self.frame_rate)
            return
        
        if self.dot_full <= self.dot_catched:
            self.game_over()
        
        for ghost in self.enemies:
            ghost.update()
        
        delta = self.clock.tick(self.frame_rate) / 1000
        self.time_last_move += delta
        self.time_last_ghost_move += delta
        
        self.update_ghost_mode()
        self.frightened_mode_frames += 1
        # print(self.ghost_mode)
        
        self.total_frames += 1
        
        self.showDotCount += 1
        
        if self.showDotCount >= self.showDotDelay:
            self.showDotCount = 0
            self.showDot = not self.showDot
            
        if self.time_last_move >= (1 / self.player_speed) * self.player.speed:
            self.player.move()
            self.time_last_move -= (1 / self.player_speed) * self.player.speed
        
        try:
            if self.time_last_ghost_move >= (1 / self.ghost_speed) * self.enemies[0].speed:
                for ghost in self.enemies:
                        ghost.move()
                self.time_last_ghost_move -= (1 / self.ghost_speed) * self.enemies[0].speed
        except IndexError:
            pass
        self.player.update_anim()
        self.check_collision()        
        
    def game_over(self):
        self.pause = True
        self.wait_frames = 30
        self.player_dead = True
        self.lives -= 1
    
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
                    self.dot_full += 1
                elif letter == "D":
                    row_temp[i] = (Tyle("dot"))
                elif letter == "E":
                    row_temp[i] = (Tyle("empty"))
                elif letter == "G":
                    row_temp[i] = ((Tyle("ghost_house")))
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
                self.store_highscore()
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
            
            if not self.pause:
                if event.type == pygame.KEYDOWN:
                    movementKeys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
                    
                    self.pause = False

                    for i, key in enumerate(movementKeys):
                        if event.key == key:
                            self.player.new_dir = i
    
    def set_ghost_mode(self, mode):
        self.ghost_mode = mode
        for ghost in self.enemies:
            if not ghost.mode == 1:
                ghost.mode = mode
            if self.frightened_mode_frames > 5 * 60:
                self.ghost_eat_points = 200
                ghost.mode = mode
    
    def update_ghost_mode(self):
        time_seconds = self.total_frames / 60
        mode = 0
        for el in self.ghost_mode_time:
            if time_seconds >= el[0]:
                mode = el[1]
        if mode == None:
            mode = 2
        self.set_ghost_mode(mode)
    
    def check_collision(self):
        pos = (self.player.x, self.player.y)
        try:
            if self.grid[round(pos[1])][round(pos[0])].type == "coin":
                self.grid[round(pos[1])][round(pos[0])] = Tyle("empty")
                self.score += 10
                self.wait_frames = 1
                self.dot_catched += 1
            
            if self.grid[round(pos[1])][round(pos[0])].type == "dot":
                self.grid[round(pos[1])][round(pos[0])] = Tyle("empty")
                self.set_ghost_mode(1)
                self.wait_frames = 3
                self.frightened_mode_frames = 0
        except IndexError:
            pass
        
        for ghost in self.enemies:
            if ghost.eaten:
                continue
            if self.player.x + 1 >= ghost.x and self.player.x <= ghost.x + 1 and self.player.y + 1 >= ghost.y and self.player.y <= ghost.y + 1:
                if ghost.mode == 1:
                    ghost.eaten = True
                    ghost.safe_zone = True
                    self.wait_frames = 30
                    self.score += self.ghost_eat_points
                    self.ghost_eat_points += 200
                else:
                    self.game_over()
    
    def render(self):
        self.renderer.new_screen()
        self.renderer.draw_background()
        self.renderer.draw_grid(self.grid)
        self.renderer.draw_player()
        self.renderer.draw_ghosts()
        # self.renderer.draw_grid_lines()
        self.renderer.draw_grame_info()
    
    def update(self):
        pygame.display.flip()
    

class Tyle(object):
    def __init__(self, tyle_type):
        self.colors = {"coin": (242, 168, 132), "empty": (0, 0, 0), "dot": (242, 168, 132)}
        self.type = tyle_type
        self.color = self.colors.get(tyle_type, (0, 0, 0))