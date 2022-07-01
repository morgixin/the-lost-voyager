from tracemalloc import start
import pygame, sys
from pygame.locals import *

from Button import Button
from game import game

clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption("The Lost Voyager")
icon = pygame.image.load("./assets/img/icon.png")
pygame.display.set_icon(icon)
screenWidth = 908
screenHeight = 512
screen = pygame.display.set_mode((screenWidth, screenHeight))

bg = pygame.image.load("./assets/img/Menu.png")

buttons = pygame.sprite.Group()
startBtn = Button(90, 160, "jogar")
aboutBtn = Button(90, 214, "sobre")
exitBtn = Button(90, 268, "sair")
buttons.add(startBtn, aboutBtn, exitBtn)

click = False

def main_menu():
    running = True
    while running:
        mouseX, mouseY = pygame.mouse.get_pos()

        if startBtn.rect.collidepoint((mouseX, mouseY)):
            startBtn.onHover()
            aboutBtn.notOnHover()
            exitBtn.notOnHover()
            if click:
                startBtn.notOnHover()
                game()
        elif aboutBtn.rect.collidepoint((mouseX, mouseY)):
            aboutBtn.onHover()
            startBtn.notOnHover()
            exitBtn.notOnHover()
            if click:
                aboutBtn.notOnHover()
                options()
        elif exitBtn.rect.collidepoint((mouseX, mouseY)):
            exitBtn.onHover()
            startBtn.notOnHover()
            aboutBtn.notOnHover()
            if click:
                running = False

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        buttons.draw(screen)
        buttons.update()
        pygame.display.flip()
        clock.tick(60)


def options():
    running = True

    while running:
        about = pygame.image.load("./assets/img/sobre.png")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.blit(about, (234, 160))
        pygame.display.flip()
        clock.tick(60)

main_menu()
