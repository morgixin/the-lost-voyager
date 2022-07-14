from re import S
import pygame
from pygame.locals import *

class AnimatedItem(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.isAnimating = False
        self.endedAnimation = False
        self.reverseAnimation = False

        self.sprites = []
        self.currentSprite = 0


    def getItemImages(self, name):
        self.image = pygame.image.load('./assets/items/'+name+'/1.png')
        self.getSprites(name)


    def getSprites(self, name):
        url = "./assets/items/"+name+"/"

        for i in range(1,9):
            self.sprites.append(pygame.image.load(url+str(i)+".png"))


    def animate(self):
        self.isAnimating = True
        self.endedAnimation = False
        if self.reverseAnimation:
            self.currentSprite = len(self.sprites)

    def update(self):
        if self.isAnimating:
            if not self.reverseAnimation:
                self.currentSprite += 0.1
                if self.currentSprite >= len(self.sprites):
                    self.currentSprite = 0
                    self.isAnimating = False
                    self.endedAnimation = True
                    self.reverseAnimation = True
                else:
                    self.image = self.sprites[int(self.currentSprite)]
                    self.endedAnimation = False
            else:
                self.currentSprite -= 0.1
                if self.currentSprite <= 0:
                    self.isAnimating = False
                    self.currentSprite = 0
                    self.reverseAnimation = False
                else:
                    self.image = self.sprites[int(self.currentSprite)]
                    self.endedAnimation = False