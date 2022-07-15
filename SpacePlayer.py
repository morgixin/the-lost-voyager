import pygame, json, os
from pygame.locals import *

pygame.init()

screenWidth = 908
screenHeight = 512
WIDTH, HEIGHT = 400, 400

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)

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

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and (self.rect.x + 5 + self.rect.width < screenWidth/2 + WIDTH/2):
                    self.movePlayer('x', 1)
                elif event.key == pygame.K_LEFT and (self.rect.x - 5 > screenWidth/2 - WIDTH/2):
                    self.movePlayer('x', -1)
                elif event.key == pygame.K_UP and (self.rect.y - 5 > screenHeight/2 - HEIGHT/2):
                    self.movePlayer('y', -1)
                elif event.key == pygame.K_DOWN and (self.rect.y + 5 + self.rect.height + 15 < screenHeight/2 + HEIGHT/2):
                    self.movePlayer('y', 1)
                if event.key == pygame.K_z:
                    self.shoot()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == controllerKeys['left_arrow'] and (self.rect.x - 5 > screenWidth/2 - WIDTH/2):
                    self.movePlayer('x', -1)
                elif event.button == controllerKeys['right_arrow'] and (self.rect.x + 5 + self.rect.width < screenWidth/2 + WIDTH/2):
                    self.movePlayer('x', 1)
                elif event.button == controllerKeys['up_arrow'] and (self.rect.y - 5 > screenHeight/2 - HEIGHT/2):
                    self.movePlayer('y', -1)
                elif event.button == controllerKeys['down_arrow'] and (self.rect.y + 5 + self.rect.height + 15 < screenHeight/2 + HEIGHT/2):
                    self.movePlayer('y', 1)
                elif event.button == controllerKeys['x']:
                    self.shoot()

            analogKeys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }
            if event.type == pygame.JOYAXISMOTION:
                analogKeys[event.axis] = event.value
                if abs(analogKeys[0]) > .4: 
                    # o abs captura movimento tanto da direita quanto da esquerda
                    if analogKeys[0] < -0.7 and (self.rect.x - 5 > screenWidth/2 - WIDTH/2):
                        self.movePlayer('x', -1)
                    elif analogKeys[0] > 0.7 and (self.rect.x + 5 + self.rect.width < screenWidth/2 + WIDTH/2):
                        self.movePlayer('x', 1)
                    if analogKeys[1] < -0.7 and (self.rect.y - 5 > screenHeight/2 - HEIGHT/2):
                        self.movePlayer('y', -1)
                    elif analogKeys[1] > 0.7 and (self.rect.y + 5 + self.rect.height + 15 < screenHeight/2 + HEIGHT/2):
                        self.movePlayer('y', 1)

    def update(self, window):
        super().update(window)
        # self.getInput()
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y + self.rect.height + 10, self.rect.width, 10))
        pygame.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y + self.rect.height + 10, self.rect.width * (self.health/self.max_health), 10))