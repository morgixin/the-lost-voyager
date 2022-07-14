import pygame
from pygame.locals import *

from Ship import Ship

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(42, 17, x, y, health)
        self.ship_img = pygame.image.load("./assets/spaceinvaders/ship.png")
        self.laser_img = pygame.image.load("./assets/spaceinvaders/shot.png")
        # self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.rect = self.ship_img.get_rect()
        self.rect.topleft = [x, y]

    def move_lasers(self, speed, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.offscreen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.rect.colliderect(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            return 15
        return 0

    def update(self, window):
        super().update(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y + self.rect.height + 10, self.rect.width, 10))
        pygame.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y + self.rect.height + 10, self.rect.width * (self.health/self.max_health), 10))