import pygame

pygame.init()

screenWidth = 908
screenHeight = 512
sprites = []

def getSprites():
    for i in range(2,12):
        sprites.append(pygame.image.load(f"./assets/earth/{i}.png").convert_alpha())

def displayEarthExplosion(screen):
    screen.fill(0)
    getSprites()

    for i in range(10):
        screen.blit(sprites[i], (screenWidth/2 - 200, screenHeight/2 - 200))
        pygame.display.update()
        pygame.time.delay(900)
