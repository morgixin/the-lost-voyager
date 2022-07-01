import pygame
from pygame.locals import *

class Emote(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([32, 32])
        self.sprites = []
        self.isAnimating = False
        self.currentSprite = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def setSprite(self, emote):
        url = "./assets/emotes/"
        if emote == "attention":
            url += "attention/"
        if emote == "zzz":
            url += "zzz/"
        if emote == "drop":
            url += "drop/"

        self.sprites.append(pygame.image.load(url+"1.png"))
        self.sprites.append(pygame.image.load(url+"2.png"))
        self.sprites.append(pygame.image.load(url+"3.png"))

    def animate(self):
        self.isAnimating = True

    def update(self):
        if self.isAnimating:
            self.currentSprite += 0.05
            if self.currentSprite >= len(self.sprites):
                self.kill()
            else:
                self.image = self.sprites[int(self.currentSprite)]

