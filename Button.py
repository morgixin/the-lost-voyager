import pygame
from pygame.locals import *

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__()
        self.image = pygame.Surface([53, 94])
        self.name = name
        self.image = pygame.image.load("./assets/btn/"+name+".png")

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
    
    def onHover(self):
        self.image = pygame.image.load("./assets/btn/"+self.name+"-hover.png")


    def notOnHover(self):
        self.image = pygame.image.load("./assets/btn/"+self.name+".png")


    # def update(self):
    #     self.update()