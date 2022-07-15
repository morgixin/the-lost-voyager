import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([78, 168])
        self.spritesRight = []
        self.spritesLeft = []

        self.isWalkingLeft = False
        self.isWalkingRight = False
        self.isAnimating = False
        self.speed = 1

        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/idle.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 1.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 2.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 3.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 4.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 5.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 6.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 7.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 1.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 2.png'))
        self.spritesRight.append(pygame.image.load('./assets/chris-sprites/walk 3.png'))

        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/idleLeft.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 1 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 2 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 3 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 4 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 5 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 6 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 7 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 1 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 2 left.png'))
        self.spritesLeft.append(pygame.image.load('./assets/chris-sprites/walk 3 left.png'))

        self.currentSprite = 0
        if self.isWalkingLeft:
            self.image = self.spritesLeft[self.currentSprite]
        else:
            self.image = self.spritesRight[self.currentSprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
   

    def setDirection(self, direction):
        if direction == "NONE":
            self.isAnimating = False
            if self.isWalkingLeft:
                self.image = self.spritesLeft[0]
            if self.isWalkingRight:
                self.image = self.spritesRight[0]
            
            self.isWalkingLeft = False
            self.isWalkingRight = False
        elif direction == "LEFT":
            self.isWalkingLeft = True
            self.isWalkingRight = False
        elif direction == "RIGHT":
            self.isWalkingLeft = False
            self.isWalkingRight = True
        

    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.setDirection("RIGHT")
        elif keys[pygame.K_LEFT]:
            self.setDirection("LEFT")

        if self.rect.x > 250:
            if self.isWalkingLeft:
                self.rect.x -= self.speed
        else:
            self.rect.x = 251
        if self.rect.x < 908 - self.rect.width:
            if self.isWalkingRight:
                self.rect.x += self.speed
        else:
            self.rect.x = 908 - 1 - self.rect.width


    def animate(self):
        self.isAnimating = True


    def update(self):
        self.getInput()

        if self.isAnimating:
            self.currentSprite += 0.2
            if self.currentSprite >= len(self.spritesRight):
                self.currentSprite = 0

            if self.isWalkingLeft:
                self.image = self.spritesLeft[int(self.currentSprite)]
            else:
                self.image = self.spritesRight[int(self.currentSprite)]
        
