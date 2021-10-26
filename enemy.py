import math

class Ghost(object):
    def __init__(self, ghost_type, game) -> None:
        self.x = 14
        self.y = 17
        
        self.__game = game
        
        self.animState = 0
        self.__animDelay = 10
        self.__animCount = 0
        
        self.speed = game.player.speed
        self.direction = 2 # Left, Right, Up, Down
        self.__player = self.__game.player
        self.target = (self.__player.x, self.__player.y)
        
        self.type = ghost_type
        
        self.safe_zone = True
        
        self.move()
        
        self.state = 0 # Scatter, Chase
    
    def canMove(self, row, col):
        if (col, row) in [(13, 15), (14, 15)] and self.safe_zone:
            return True
        if col == -1 or col >= self.__game.size[0]:
            return True
        if self.__game.grid[int(row)][int(col)].type == "border":
            return False
        return True
    
    def update(self):
        self.__animCount += 1
        
        if self.__animCount >= self.__animDelay:
            self.animState = 1 - self.animState
            self.__animCount = 0
        
    def move(self):
        if self.x % 1.0 == 0 and self.y % 1 == 0:
            
            # self.__game.pause = True
            
            self.calcTarget()
                        
            dirPossible = [0, 1, 2, 3]
            dirPossible.remove((1 + 2 * (self.direction // 2)) - self.direction % 2)
            
            calculatedDistance = {x:None for x in dirPossible}
            dirVectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            if self.x == 0 or self.x == self.__game.size[0]:
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
                        curDist = self.distToTarget(vector)
                        calculatedDistance[direction] = curDist
                    else:
                        del calculatedDistance[direction]
                
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
                            
        else:
            if self.direction == 0:
                self.x -= self.speed
            elif self.direction == 1:
                self.x += self.speed
            elif self.direction == 2:
                self.y -= self.speed
            elif self.direction == 3:
                self.y += self.speed
        
        self.x %= self.__game.size[0]
        self.y %= self.__game.size[1]
        
        if (self.x, self.y) in [(13, 15), (14, 15)]:
            self.safe_zone = False
    
    def distToTarget(self, vector):
        x1 = self.target[0]
        x2 = self.x + vector[0]
        y1 = self.target[1]
        y2 = self.y + vector[1]
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return dist
    
    def calcTarget(self):
        if self.__game.ghosts_frightened:
            difx = self.__player.x - self.x
            dify = self.__player.y - self.y
            self.target = (self.x - difx, self.y - dify)
        else:
            if self.type == 0:
                self.target = (self.__player.x, self.__player.y)