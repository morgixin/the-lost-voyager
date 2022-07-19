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
sprites = []
sprites.append(pygame.image.load("./assets/1.png").convert_alpha())
sprites.append(pygame.image.load("./assets/2.png").convert_alpha())

def startAnimation():
    screen.fill(0)
    pygame.time.delay(1000)

    for i in range(2):
        screen.blit(sprites[i], (screenWidth/2 - 250, screenHeight/2 - 250))
        pygame.display.update()
        pygame.time.delay(1500)

def startStory():
    running = True
    font = pygame.font.Font("./assets/font/Pixeled.ttf", 20)
    introString = '''A quilometros de quilometros de casa,
    o astronauta Chris Hadfield embarca em 
    uma nova jornada pela  empresa ExoSpace 
    com destino ao infinito sideral.

    Com objetivo de estudar a vida de Marte, 
    Chris segue ansioso para analisar e reportar
    suas descobertas sobre o planeta tao 
    almejado pela humanidade. 
    
    "Talvez descubram maneiras novas de 
    sobrevivencia utilizando o solo de Marte. 
    É definitivamente uma honra viver isso,
    pisar em solo marciano... 
    Vejamos o que ele tem a oferecer"

    E com esse animo, ainda faltam 200 dias 
    para chegar ao seu destino.
    '''

    deltaY = screen.get_rect().centery + 50

    while running:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
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