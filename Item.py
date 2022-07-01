import pygame
from pygame.locals import *

class Item(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]


    def getItemImage(self, name):
        self.image = pygame.image.load('./assets/items/'+name+'.png')



