import json, os, sys
import pygame
from pygame.locals import *

from Emote import Emote 
from Player import Player
from Item import Item
from AnimatedItem import AnimatedItem
from spaceInvaders import main_menu

pygame.init()
clock = pygame.time.Clock()

# Gerando a janela do jogo
screenWidth = 908
screenHeight = 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("The Lost Voyager")
icon = pygame.image.load("./assets/img/icon.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("./assets/img/nave 5.png")

# Obtenção dos elementos da interface
movingSprites = pygame.sprite.Group()
player = Player(260, 230)
movingSprites.add(player)

movingItems = pygame.sprite.Group()
door = AnimatedItem(104, 512, 736, 0)
door.getItemImages("door")
movingItems.add(door)



# Inicializando o controle
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)


textLabels = []
dialRect = pygame.Rect(0, 400, screenWidth, 118)

def drawText(text):
    font = pygame.font.Font("./assets/font/Pixeled.ttf", 15)
    text_label = font.render(text, 1, (255,255,255))
    sub = "[clique enter]"
    sub_label = font.render(sub, 1, (255,255,255))
    textLabels.append(text_label)
    textLabels.append(sub_label)


def game():
    running = True
    awaitEnterKey = False
    click = False
    while running:
        screen.fill(0)
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
                    # checa se o jogador esta colidindo com 
                    # os elementos interativos na tela
                    if player.rect.colliderect(door):
                        if not door.endedAnimation:
                            door.animate()
                        else:
                            door.animate()
                    if 256 <= int(player.rect.x) <= 386: # area do painel de comando
                        drawText("Sempre bom descansar a mente com um pouco de videogame.")
                        awaitEnterKey = True
                if event.key == pygame.K_x:
                    emote = Emote(player.rect.x + player.rect.width/3, player.rect.y - 45)
                    emote.setSprite("zzz")
                    emote.animate()
                    movingSprites.add(emote)
                if event.key == pygame.K_RETURN and awaitEnterKey:
                    textLabels.clear()
                    click = True
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
                    if player.rect.colliderect(door):
                        if not door.endedAnimation:
                            door.animate()
                            emote.setSprite("attention")
                            emote.animate()
                            movingSprites.add(emote)
                        else:
                            door.animate()
                            emote.setSprite("attention")
                            emote.animate()
                            movingSprites.add(emote)
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
                
        # checa se esta colidindo com os elementos principais
        if player.rect.colliderect(door) and not door.endedAnimation:
            player.isWalkingLeft = False
            player.isWalkingRight = False
            if player.rect.x <= door.rect.x + door.rect.width/2:
                player.rect.x -= 1
            else:
                player.rect.x = door.rect.x + door.rect.width + 1

        if 256 <= int(player.rect.x) <= 386 and click: # area do painel de comando
            main_menu()
            click = False

        if player.rect.x < screenWidth - 50:
            bgX = 250 - player.rect.x-1
            for item in movingItems:
                item.rect.x = 250 + 736 - player.rect.x-1
        screen.blit(bg, (bgX, 0))
        movingSprites.draw(screen)
        movingSprites.update()
        movingItems.draw(screen)
        movingItems.update()
        if textLabels != []:
            pygame.draw.rect(screen, (0,0,0), dialRect)
            for i in range(len(textLabels)):
                screen.blit(textLabels[i], (35, 410+25*i))


        pygame.display.flip()
        clock.tick(60)
