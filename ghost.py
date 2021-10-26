import math, random


class Ghost(object):
    def __init__(self, ghost_type, game) -> None:
        self.x = random.randint(12, 15)
        self.y = 17
        
        self.game = game
        
        self.animState = 0
        self.__animDelay = 10
        self.__animCount = 0
        
        self.speed = game.player.speed
        self.direction = 2 # Left, Right, Up, Down
        self.__player = self.game.player
        self.target = (self.__player.x, self.__player.y)
        
        self.eaten = False
        
        self.__scatter_target = [(25, -1), (2, -1), (27, 34), (0, 34)]
        
        self.mode = 0 # scatter, frightened, chase
        
        self.first_frighten = True
        
        self.type = ghost_type # red, pink, blue, orange
        
        self.safe_zone = True
        
        self.move()
        
        self.state = 0 # Scatter, Chase
    
    def canMove(self, row, col):
        if (col, row) in [(13, 15), (14, 15)] and self.safe_zone:
            return True
        if col == -1 or col >= self.game.size[0]:
            return True
        if self.game.grid[int(row)][int(col)].type == "border":
            return False
        return True
    
    def update(self):
        self.__animCount += 1
        
        if self.__animCount >= self.__animDelay:
            self.animState = 1 - self.animState
            self.__animCount = 0
        
    def move(self):
        if self.x % 1.0 == 0 and self.y % 1 == 0:

            try:
                if self.game.grid[int(self.y)][int(self.x)].type == "ghost_house" and self.eaten:
                    self.eaten = False
                    self.safe_zone = True
                    self.mode = 2
            except IndexError:
                pass
            
            dirPossible = [0, 1, 2, 3]
            
            if (not self.mode == 1) or self.eaten:
                self.calcTarget()
                dirPossible.remove((1 + 2 * (self.direction // 2)) - self.direction % 2)
            
            if not self.first_frighten:
                try:
                    dirPossible.remove((1 + 2 * (self.direction // 2)) - self.direction % 2)
                except:
                    pass
            
            calculatedDistance = {x:None for x in dirPossible}
            dirVectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            if self.x == 0 or self.x == self.game.size[0]:
                try:
                    dirPossible.remove(2)
                except:
                    pass
                try:
                    dirPossible.remove(3)
                except:
                    pass
            
            if len(dirPossible) == 1:
                self.direction == dirPossible[0]
            
            else:
                for direction in dirPossible:
                    vector = dirVectors[direction]
                    if self.canMove(self.y + vector[1], self.x + vector[0]):
                        calculatedDistance[direction] = self.distToTarget(vector)
                    else:
                        del calculatedDistance[direction]
                if self.mode == 1 and not self.eaten:
                    backDir = (1 + 2 * (self.direction // 2)) - self.direction % 2
                    if (backDir in calculatedDistance and calculatedDistance[backDir] != None) and self.first_frighten:
                        self.direction = backDir
                        self.first_frighten = False
                    else:
                        self.direction = random.choice([x for x in calculatedDistance if calculatedDistance[x] != None])
                else:
                    calculatedDistance = sorted(calculatedDistance.items(), key=lambda x: x[1])
                    self.direction = calculatedDistance[0][0]
            
            if self.direction == 0:
                self.x -= self.speed
            elif self.direction == 1:
                self.x += self.speed
            elif self.direction == 2:
                self.y -= self.speed
            elif self.direction == 3:
                self.y += self.speed
            if self.eaten:
                if self.direction == 0:
                    self.x -= self.speed
                elif self.direction == 1:
                    self.x += self.speed
                elif self.direction == 2:
                    self.y -= self.speed
                elif self.direction == 3:
                    self.y += self.speed
                            
        else:
            if self.direction == 0:
                self.x -= self.speed
            elif self.direction == 1:
                self.x += self.speed
            elif self.direction == 2:
                self.y -= self.speed
            elif self.direction == 3:
                self.y += self.speed

            if not (self.x % 0.5 == 0 and self.y % 0.5 == 0) and self.eaten:
                if self.direction == 0:
                    self.x -= self.speed
                elif self.direction == 1:
                    self.x += self.speed
                elif self.direction == 2:
                    self.y -= self.speed
                elif self.direction == 3:
                    self.y += self.speed
                            
        
        self.x %= self.game.size[0]
        self.y %= self.game.size[1]
        
        if (self.x, self.y) in [(13, 15), (14, 15)]:
            if not self.eaten:
                self.safe_zone = False
    
    def distToTarget(self, vector):
        x1 = self.target[0]
        x2 = self.x + vector[0]
        y1 = self.target[1]
        y2 = self.y + vector[1]
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return dist
    
    def calcTarget(self):
        if self.eaten:
            self.target = (13.5, 17)
        elif (self.game.grid[int(self.y)][int(self.x)].type == "ghost_house"):
            self.target = (13.5, 14)
        elif self.mode == 0:
            self.target = self.__scatter_target[self.type]
        elif self.mode == 2:
            if self.type == 0:
                self.target = (self.__player.x, self.__player.y)
            elif self.type == 1:
                player = self.__player
                if player.direction == 0:
                    self.target = (player.x - 4, player.y)
                elif player.direction == 1:
                    self.target = (player.x + 4, player.y)
                elif player.direction == 2:
                    self.target = (player.x + 4, player.y - 4)
                elif player.direction == 3:
                    self.target = (player.x, player.y + 4)
            elif self.type == 2:
                dirVectors = [(-1, 0), (1, 0), (-1, -1), (0, 1)]
                temp_tyle = (self.__player.x + dirVectors[self.__player.direction][0] * 2, self.__player.y + dirVectors[self.__player.direction][1] * 2)
                blinky_tyle = (self.game.enemies[0].x, self.game.enemies[0].y)
                vector = tuple(map(lambda i, j: i - j, temp_tyle, blinky_tyle))
                self.target = tuple(map(lambda i, j: i + j, vector, temp_tyle))
            elif self.type == 3:
                x1 = self.__player.x
                x2 = self.x
                y1 = self.__player.y
                y2 = self.y
                dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if dist <= 8:
                    self.target == self.__scatter_target[3]
                else:
                    self.target = (x1, y1)