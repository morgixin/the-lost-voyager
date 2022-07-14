import pygame
from Laser import Laser

class Ship:
    COOLDOWN = 30

    def __init__(self, height, width, x, y, health=100):
        self.health = health
        self.ship_img = pygame.Surface([width, height])
        self.laser_img = pygame.Surface([4, 15])
        self.lasers = []
        self.cool_down_counter = 0

        self.rect = self.ship_img.get_rect()
        self.rect.topleft = [x, y]

    def update(self, window):
        window.blit(self.ship_img, (self.rect.x, self.rect.y))
        for laser in self.lasers:
            laser.update(window)

    def move_lasers(self, speed, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.offscreen():
                self.lasers.remove(laser)
            elif laser.rect.colliderect(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.rect.x + self.rect.width/2, self.rect.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1