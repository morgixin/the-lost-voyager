import pygame
from Ship import Ship 
from Laser import Laser

class Enemy(Ship):
    COLOR_MAP = {
                "red": pygame.image.load("./assets/spaceinvaders/enemies/red.png"),
                "white": pygame.image.load("./assets/spaceinvaders/enemies/white.png"),
                "blue": pygame.image.load("./assets/spaceinvaders/enemies/blue.png")
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(49, 49, x, y, health)
        self.ship_img = self.COLOR_MAP[color]
        self.laser_img = pygame.image.load("./assets/spaceinvaders/enemyshot.png")

        self.rect = self.ship_img.get_rect()
        self.rect.topleft = [x, y]

    def move(self, speed):
        self.rect.y += speed

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.rect.x-20, self.rect.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1