import pygame

class SpriteLoader(object):
    def __init__(self):
        
        self.sprite_img = pygame.image.load("Assets/SPRITE_SHEET.png")
        
        self.PlayerImg = self.load_player_img()
        self.GhostImg = self.load_ghost_img()
        self.Boards = self.load_board_img()
        self.Letters = self.load_letter_img()
        self.TitleImg = self.load_title_img()
        # self.Numbers = self.load_number_img()
    
    def load_title_img(self):
        startX = 0
        startY = 253
        offsetL = 0
        offsetR = 0
        offsetT = 0
        offsetB = 0
        width, height = 185, 50
    
        
        rect = pygame.Rect(startX, startY, width, height)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sprite_img, (0, 0), rect)
        image.set_colorkey((0, 0, 0))
        
        return image
        
    def load_player_img(self):
        # rect = pygame.Rect(rectangle)
        # image = pygame.Surface(rect.size).convert()
        # image.blit(self.sheet, (0, 0), rect)
        # if colorkey is not None:
        #     if colorkey is -1:
        #         colorkey = image.get_at((0,0))
        #     image.set_colorkey(colorkey, pygame.RLEACCEL)
        startX = 684
        startY = 0
        offsetL = 1
        offsetR = 0
        offsetT = 1
        offsetB = 0
        width, height = 15, 15
        
        img_list = {}

        pos = [
                (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0),
                (0, 1), (1, 1),
                (0, 2), (1, 2),
                (0, 3), (1, 3)
            ]
        
        for (i, j) in pos:
            rect = pygame.Rect(i * (width + offsetL + offsetR) + startX + offsetL, j * (height + offsetT + offsetB) + startY + offsetT, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sprite_img, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            img_list[(i, j)] = image
            
        return img_list

    def load_player_img_at(self, rot, animc, dead, deadAnim):
        if dead:
            img = self.PlayerImg[(3 + deadAnim, 0)]
            img = pygame.transform.rotate(img, [90, -90, 0, 180][rot])
            return img
        if animc >= 2:
            return self.PlayerImg[(2, 0)]
        rotation_lookup = [1, 0, 2, 3]
        rot = rotation_lookup[rot]
        return self.PlayerImg[(animc, rot)]
    
    def load_letter_img(self):
        startX = 230
        startY = 256
        offsetL = 0
        offsetR = 1
        offsetT = 0
        offsetB = 1
        width, height = 7, 7
        
        img_list = {}
        
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        pos = [
                (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0),
                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
                (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2)
            ]

        for ind, (i, j) in enumerate(pos):
            rect = pygame.Rect(i * (width + offsetL + offsetR) + startX + offsetL, j * (height + offsetT + offsetB) + startY + offsetT, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sprite_img, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            img_list[letters[ind]] = image
            
        return img_list
    
    def load_letter_img_at(self, letter_or_number):
        return self.Letters[str(letter_or_number)]
    
    def load_board_img(self):
        startX = 0
        startY = 0
        offsetL = 0
        offsetR = 1
        offsetT = 0
        offsetB = 0
        width, height = 227, 252
        
        img_list = {}
        
        pos = [
                (0, 0), (1, 0), (2, 0)
            ]

        for ind, (i, j) in enumerate(pos):
            rect = pygame.Rect(i * (width + offsetL + offsetR) + startX + offsetL, j * (height + offsetT + offsetB) + startY + offsetT, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sprite_img, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            img_list[ind] = image
        
        return img_list

    def load_board_img_at(self, ind):
        return self.Boards[ind]

    def load_ghost_img(self):
        startX = 684
        startY = 0
        offsetL = 1
        offsetR = 0
        offsetT = 1
        offsetB = 0
        width, height = 15, 15
        
        img_list = {}

        pos = [
                (0, 4),(1, 4),(2, 4),(3, 4),(4, 4),(5, 4),(6, 4),(7, 4),(8, 4),(9, 4),(10, 4),(11, 4),
                (0, 5),(1, 5),(2, 5),(3, 5),(4, 5),(5, 5),(6, 5),(7, 5),(8, 5),(9, 5),(10, 5),(11, 5),
                (0, 6),(1, 6),(2, 6),(3, 6),(4, 6),(5, 6),(6, 6),(7, 6),
                (0, 7),(1, 7),(2, 7),(3, 7),(4, 7),(5, 7),(6, 7),(7, 7),(8, 7),(9, 7),(10, 7),(11, 7)
            ]
        
        for (i, j) in pos:
            rect = pygame.Rect(i * (width + offsetL + offsetR) + startX + offsetL, j * (height + offsetT + offsetB) + startY + offsetT, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sprite_img, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            img_list[(i, j - 4)] = image
            
        return img_list

    def load_ghost_img_at(self, ghost):
        color, animState, direction, mode, flicker = ghost.type, ghost.animState, ghost.direction, ghost.mode, ghost.flicker_state
        rotation_lookup = [1, 0, 2, 3]
        direction = rotation_lookup[direction]
        if ghost.eaten:
            return self.GhostImg[(8+direction, 1)]
        if mode == 1:
            if color <= 1:
                if flicker:
                    return self.GhostImg[(10+animState, 0)]
                return self.GhostImg[(8+animState, 0)]
            else:
                if flicker:
                    return self.GhostImg[(8+animState, 0)]
                return self.GhostImg[(10+animState, 0)]
        else:
            return self.GhostImg[(direction*2 + animState, color)]

    def load(self, Element, *args, Rotation=0, AnimCount=0, letter="", boardInd=0, ghost=[0, 0, 0, False], PlayerDead=False, PlayerDeadAnim=0):
        if Element.lower() == "pacman":
            return self.load_player_img_at(Rotation, AnimCount, PlayerDead, PlayerDeadAnim)
        elif Element.lower() == "letter":
            if letter == "":
                return False
            else:
                return self.load_letter_img_at(letter.upper())
        elif Element.lower() == "bg":
            return self.load_board_img_at(boardInd)
        elif Element.lower() == "ghost":
            return self.load_ghost_img_at(ghost)
        raise KeyError("unknown sprite type")