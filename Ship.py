import pygame, os, json
from Laser import Laser

pygame.init()

screenWidth = 908
screenHeight = 512
WIDTH, HEIGHT = 400, 400

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)

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
        # self.getInput()
        window.blit(self.ship_img, (self.rect.x, self.rect.y))
        for laser in self.lasers:
            laser.update(window)

    def movePlayer(self, axis, orientation):
        if axis == 'x':
            if orientation < 0:
                self.rect.x -= 5
            else:
                self.rect.x += 5
        else:
            if orientation < 0:
                self.rect.y -= 5
            else:
                self.rect.y += 5
        

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