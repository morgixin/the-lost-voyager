import pygame, os, json
from pygame.locals import *
import random

from SpacePlayer import Player
from Enemy import Enemy

clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption("The Lost Voyager")
icon = pygame.image.load("./assets/img/icon.png")
pygame.display.set_icon(icon)
screenWidth = 908
screenHeight = 512
screen = pygame.display.set_mode((screenWidth, screenHeight))

BG = pygame.image.load("./assets/spaceinvaders/background-black.png")

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)

def collide(obj1, obj2):
    return obj1.rect.colliderect(obj2)

def spaceinvaders():
    run = True
    WIDTH, HEIGHT = 400, 400
    points = 0
    lives = 3
    main_font = pygame.font.Font("./assets/font/Pixeled.ttf", 15)
    lost_font = pygame.font.Font("./assets/font/Pixeled.ttf", 25)

    enemies = []
    wave_length = 3
    enemy_speed = 1

    player_vel = 5
    laser_vel = 4

    player = Player(300, 430)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        screen.fill(0)
        screen.blit(BG, (screenWidth/2 - WIDTH/2, screenHeight/2 - HEIGHT/2))
        # draw text
        lives_label = main_font.render(f"Vidas: {lives}", 1, (255,255,255))
        point_label = main_font.render(f"Pontos: {points}", 1, (255,255,255))

        screen.blit(lives_label, (screenWidth/2 - WIDTH/2 + 10, screenHeight/2 - HEIGHT/2))
        screen.blit(point_label, (screenWidth/2 + WIDTH/2 - 130, screenHeight/2 - HEIGHT/2))

        for enemy in enemies:
            enemy.update(screen)

        if lost:
            lost_label = lost_font.render("Voce perdeu!", 1, (255,255,255))
            score_label = main_font.render(f"Pontos totais: {points}", 1, (255,255,255))
            screen.blit(lost_label, (screenWidth/2 - lost_label.get_width()/2, screenHeight/2 - lost_label.get_height()/2))
            screen.blit(score_label, (screenWidth/2 - score_label.get_width()/2, screenHeight/2 + 30))

    while run:
        # todo o jogo possui suporte para PS4
        # mas ainda sera implementado no minijogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # lida com botoes do teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (player.rect.x - player_vel > screenWidth/2 - WIDTH/2): # left
            player.rect.x -= player_vel
        if keys[pygame.K_RIGHT] and (player.rect.x + player_vel + player.rect.width < screenWidth/2 + WIDTH/2): # right
            player.rect.x += player_vel
        if keys[pygame.K_UP] and (player.rect.y - player_vel > screenHeight/2 - HEIGHT/2): # up
            player.rect.y -= player_vel
        if keys[pygame.K_DOWN] and (player.rect.y + player_vel + player.rect.height + 15 < screenHeight/2 + HEIGHT/2): # down
            player.rect.y += player_vel
        if keys[pygame.K_z]:
            player.shoot()
        if keys[pygame.K_x]:
            run = False
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > 60 * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            # points += 25
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(screenWidth/2 - WIDTH/2, screenWidth/2 + WIDTH/2 - 49), screenHeight/2 - HEIGHT/2, random.choice(["red", "blue", "white"]))
                enemies.append(enemy)


        for enemy in enemies[:]:
            enemy.move(enemy_speed)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.rect.y + enemy.rect.height > screenHeight/2 + HEIGHT/2:
                lives -= 1
                enemies.remove(enemy)

        points += player.move_lasers(-laser_vel, enemies)
        redraw_window()
        player.update(screen)
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    WIDTH, HEIGHT = 400, 400
    title_font = pygame.font.Font("./assets/font/Pixeled.ttf", 20)
    sub_font = pygame.font.Font("./assets/font/Pixeled.ttf", 15)
    run = True
    while run:
        screen.fill(0)
        screen.blit(BG, (screenWidth/2 - WIDTH/2, screenHeight/2 - HEIGHT/2))
        title_label = title_font.render("SPACE INVADERS", 1, (255,255,255))
        sub_label = sub_font.render("clique [Z] pra jogar e atirar!", 1, (255,255,255))
        screen.blit(title_label, (screenWidth/2 - title_label.get_width()/2, screenHeight/2 - title_label.get_height()/2))
        screen.blit(sub_label, (screenWidth/2 - sub_label.get_width()/2, screenHeight/2 + 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    spaceinvaders()
                if event.key == pygame.K_x:
                    run = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == controllerKeys['x']:
                    spaceinvaders()
                if event.button == controllerKeys['circle']:
                    run = False