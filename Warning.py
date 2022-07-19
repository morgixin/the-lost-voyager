import pygame
import sys
import os
import json
from pygame.locals import *
pygame.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)


class Warning():
    def __init__(self, warning):
        self.warningLabels = []
        self.createWarning(warning)
        self.solved = False

    def createWarning(self, text):
        warningFont = pygame.font.Font("./assets/font/Pixeled.ttf", 20)
        warning_label = warningFont.render(text, 1, (255, 255, 255))
        subFont = pygame.font.Font("./assets/font/Pixeled.ttf", 15)
        sub = "[Z] Confirma [X] Cancela"
        sub_label = subFont.render(sub, 1, (255, 255, 255))
        self.warningLabels.append(warning_label)
        self.warningLabels.append(sub_label)

    def getWarnings(self):
        return self.warningLabels

    def clearWarning(self):
        self.warningLabels.clear()

    def getInput(self):
        for event in pygame.event.get():
            # check controller input
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == controllerKeys['x']:
                    self.confirm = True
                elif event.button == controllerKeys['circle']:
                    self.clearWarning()
                # check keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.clearWarning()
                if event.key == pygame.K_z:
                    pygame.quit()
                    sys.exit()
