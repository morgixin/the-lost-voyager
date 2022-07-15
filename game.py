import json, os, sys
import pygame
from pygame.locals import *

from Emote import Emote 
from Player import Player
from Warning import Warning
from Text import TextBox
from AnimatedItem import AnimatedItem
from earthAnimation import displayEarthExplosion
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
bg = pygame.image.load("./assets/img/nave 5.jpg")

# Obtenção dos elementos da interface
movingSprites = pygame.sprite.Group()
player = Player(260, 230)
movingSprites.add(player)

movingItems = pygame.sprite.Group()
door = AnimatedItem(104, 512, 762, 0)
door.getItemImages("door")
movingItems.add(door)

font = pygame.font.Font("./assets/font/Pixeled.ttf", 20)
warnings = []
warningRect = pygame.Rect(190, 180, 500, 200)

textLabels = []
dialRect = pygame.Rect(0, 380, screenWidth, 218)

def fade(): 
    fade = pygame.Surface((screenWidth, screenHeight))
    fade.fill((0,0,0))
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        screen.fill(0)
        screen.blit(bg, (250 - player.rect.x-1, 0))
        movingSprites.draw(screen)
        movingSprites.update()
        movingItems.draw(screen)
        movingItems.update()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)


def checkCollision(days):
    # checa se o jogador esta colidindo com 
    # os elementos interativos na tela
    if player.rect.colliderect(door):
        if not door.endedAnimation:
            door.animate()
        else:
            door.animate()
    if 256 <= int(player.rect.x) <= 386: # area do painel de comando
        playSI = TextBox("Sempre bom descansar a mente com um pouco de videogame.", "Q")
        textLabels.append(playSI)
    if 250 <= int(player.rect.x) <= 255:
        if days < 3: # area da janela
            windowMsg = TextBox("A Terra é linda daqui", "T")
            textLabels.append(windowMsg)
        else:
            windowMsg = TextBox("A Terra é tao... QUE?", "A")
            textLabels.append(windowMsg)
    if 576 <= int(player.rect.x) <= 638:
        doorMsg = TextBox("O tanto de folhas que preciso organizar ai... melhor nem entrar.", "T")
        textLabels.append(doorMsg)
    if 761 <= int(player.rect.x) <= 908: # area da cama
        windowMsg = TextBox("Dormir ajuda a passar esse tempo infinito aqui.", "Q")
        textLabels.append(windowMsg)

def game():
    # Inicializando o controle
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    with open(os.path.join("ps4_keys.json"), "r+") as file:
        controllerKeys = json.load(file)

    days = 0
    running = True
    awaitConfirm = False
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
                if event.key == pygame.K_c:
                    click = True
                    emote = Emote(player.rect.x + player.rect.width/3, player.rect.y - 45)
                    emote.setSprite("attention")
                    emote.animate()
                    movingSprites.add(emote)

                    checkCollision(days)
                    awaitConfirm = True
                if event.key == pygame.K_x:
                    awaitConfirm = False
                elif event.key == pygame.K_ESCAPE:
                    if warnings == [] and not awaitConfirm:
                        warning = Warning("Deseja sair do jogo?")
                        warnings.append(warning)
                        awaitConfirm = True
            if event.type == pygame.KEYUP:
                player.setDirection("NONE")
                # click = False
            # lida com as setas do controle
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == controllerKeys['left_arrow']:
                    player.setDirection("LEFT")
                    player.animate()
                elif event.button == controllerKeys['right_arrow']:
                    player.setDirection("RIGHT")
                    player.animate()
                elif event.button == controllerKeys['triangle']:
                    emote = Emote(player.rect.x + player.rect.width/3, player.rect.y - 45)
                    emote.setSprite("attention")
                    emote.animate()
                    movingSprites.add(emote)

                    checkCollision(days)

                    awaitConfirm = True
                elif event.button == controllerKeys['circle']:
                    click = True
                    awaitConfirm = False
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == controllerKeys['left_arrow']:
                    player.setDirection("NONE")
                elif event.button == controllerKeys['right_arrow']:
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
        if textLabels != [] and textLabels[0].confirm:
            if 256 <= int(player.rect.x) <= 386: # area do painel de comando
                textLabels[0].confirm = False
                main_menu()
            if 250 <= int(player.rect.x) <= 255: # area da janela
                if days >= 3: 
                    textLabels[0].confirm = False
                    displayEarthExplosion(screen) 
                    running = False
                else:
                    textLabels[0].confirm = False
            if 761 <= int(player.rect.x) <= 908: # area da cama
                days += 1
                fade()
                textLabels[0].confirm = False

        if player.rect.x < screenWidth - 50:
            bgX = 250 - player.rect.x-1
            for item in movingItems:
                item.rect.x = 250 + 762 - player.rect.x-1
        screen.blit(bg, (bgX, 0))
        movingSprites.draw(screen)
        movingSprites.update()
        movingItems.draw(screen)
        movingItems.update()

        if textLabels != []:
            pygame.draw.rect(screen, (0,0,0), dialRect)
            if textLabels[0].getText() == []:
                textLabels.clear()
            else:
                textLabels[0].getInput()
                for i in range(len(textLabels[0].getText())):
                    screen.blit(textLabels[0].getText()[i], (35, 400+35*i))
            
        if warnings != []:
            pygame.draw.rect(screen, (0,0,0), warningRect)
            if warnings[0].getWarnings() != []:
                warnings[0].getInput()
                for i in range(len(warnings[0].getWarnings())):
                    screen.blit(warnings[0].getWarnings()[i], (260+20*i, 230+45*i))
            else:
                warnings.clear()

        day_label = font.render(f"Dia {int(days)}", 1, (255,255,255))
        screen.blit(day_label, (20,10))

        pygame.display.flip()
        clock.tick(60)
