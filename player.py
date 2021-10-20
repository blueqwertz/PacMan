class Player(object):
    def __init__(self, speed):
        self.x = 13.5
        self.y = 26
        self.speed = speed
        
        self.rotation = 0
        
        self.dir_x = 0
        self.dir_y = 0
    
    def send_key(self, index, delta):
        if index == 0:
            self.x -= delta/1000 * self.speed
        if index == 1:
            self.y -= delta/1000 * self.speed
        if index == 2:
            self.x += delta/1000 * self.speed
        if index == 3:
            self.y += delta/1000 * self.speed