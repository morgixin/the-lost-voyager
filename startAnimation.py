import pygame
from pygame.locals import *

pygame.display.set_caption("The Lost Voyager")
icon = pygame.image.load("./assets/img/icon.png")
pygame.display.set_icon(icon)
screenWidth = 908
screenHeight = 512
screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()
pygame.init()


def startAnimation():
    running = True
    font = pygame.font.Font("./assets/font/Pixeled.ttf", 20)
    introString = '''Made by Ana Beatriz e Julia da Camara
    Brought to you by Trabalhos e Demandas da UFF
    .
    .
    .
    Clica qualquer tecla ai
    '''

    deltaY = screen.get_rect().centery + 50

    while running:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False

        deltaY -= 0.5
        shown = []
        posList = []
        i = 0
        for line in introString.split("\n"):
            msg = font.render(line, True, (255,255,255))
            shown.append(msg)
            pos = msg.get_rect(center =(screen.get_rect().centerx, screen.get_rect().centery + int(deltaY) + 50*i)) 
            posList.append(pos)
            i += 1
        
        for w in range(i):
            screen.blit(shown[w], posList[w])

        pygame.display.flip()
        clock.tick(60)