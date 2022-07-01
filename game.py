import json, os, sys
import pygame
from pygame.locals import *

from Emote import Emote 
from Player import Player
from Item import Item
from AnimatedItem import AnimatedItem

pygame.init()
clock = pygame.time.Clock()

# Gerando a janela do jogo
screenWidth = 908
screenHeight = 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("The Lost Voyager")
icon = pygame.image.load("./assets/img/icon.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("./assets/img/nave 5.jpg").convert()
# bg = pygame.transform.scale(bg, (int(bg.image.get_size[0]*3), int(bg.image.get_size[1]*3)))

# Obtenção dos elementos da interface
# background = GameImage('./assets/img/fundo big.png')

movingSprites = pygame.sprite.Group()
player = Player(260, 230)
movingSprites.add(player)
# staticSprites = pygame.sprite.Group()
# bottle = Item(90, 240, 10, 20)
# bottle.getItemImage("bottle")
# staticSprites.add(bottle)

# door = AnimatedItem(104, 512, 736, 0)
# movingSprites.add(door)
# keys = window.get_keyboard()

# Inicializando o controle
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)


def game():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # lida com botoes do teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.animate()
                if event.key == pygame.K_LEFT:
                    player.animate()
                if event.key == pygame.K_z:
                    emote = Emote(player.rect.x + player.rect.width/3, player.rect.y - 45)
                    emote.setSprite("attention")
                    emote.animate()
                    movingSprites.add(emote)
                if event.key == pygame.K_x:
                    emote = Emote(player.rect.x + player.rect.width/3, player.rect.y - 45)
                    emote.setSprite("zzz")
                    emote.animate()
                    movingSprites.add(emote)
            if event.type == pygame.KEYUP:
                player.setDirection("NONE")

            # lida com as setas do controle
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == controllerKeys['left_arrow']:
                    player.setDirection("LEFT")
                    player.animate()
                if event.button == controllerKeys['right_arrow']:
                    player.setDirection("RIGHT")
                    player.animate()
                if event.button == controllerKeys['x']:
                    emote.setSprite("attention")
            if event.type == pygame.JOYBUTTONUP:
                if event.button == controllerKeys['left_arrow']:
                    player.setDirection("NONE")
                if event.button == controllerKeys['right_arrow']:
                    player.setDirection("NONE")

            # lida com o joystick do controle
            analogKeys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }
            if event.type == pygame.JOYAXISMOTION:
                analogKeys[event.axis] = event.value
                if abs(analogKeys[0]) > .4: 
                    # o abs captura movimento tanto da direita quanto da esquerda
                    # Como o jogador só se move pelo eixo x, só detecta o movimento horizontal
                    if analogKeys[0] < -0.7:
                        player.setDirection("LEFT")
                        player.animate()
                    elif analogKeys[0] > 0.7:
                        player.setDirection("RIGHT")
                        player.animate()
                    else:
                        player.setDirection("NONE")
                
            # if player.rect.collidepoint((door.rect.x, door.rect.y)):
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_z:
            #             door.animate()

        
        

        screen.fill((0,0,0))
        if player.rect.x < screenWidth-50:
            bgX = 250 - player.rect.x-1
        screen.blit(bg, (bgX, 0))
        movingSprites.draw(screen)
        movingSprites.update()

        # staticSprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
