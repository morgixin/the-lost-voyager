import pygame, os, json
from pygame.locals import *

pygame.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

with open(os.path.join("ps4_keys.json"), "r+") as file:
    controllerKeys = json.load(file)

class TextBox():
    def __init__(self, text, type):
        self.textLabels = []
        self.sub = ""
        self.checkTextType(type)
        self.confirm = False
        self.createTextBox(text)

    def checkTextType(self, type):
        if type == "T":
            self.sub = "[X] FECHAR"
        if type == "A":
            self.sub = "[Z] CONTINUAR"
        if type == "Q":
            self.sub = "CONTINUAR? [Z] SIM    [X] NAO"

    def createTextBox(self, text):
        font = pygame.font.Font("./assets/font/Pixeled.ttf", 15)
        text_label = font.render(text, 1, (255,255,255))
        sub_label = font.render(self.sub, 1, (255,255,255))
        self.textLabels.append(text_label)
        self.textLabels.append(sub_label)
    
    def clearTextBox(self):
        self.textLabels.clear()

    def getText(self):
        return self.textLabels

    def getInput(self):
        for event in pygame.event.get():
            # check keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.clearTextBox()
                if event.key == pygame.K_z:
                    self.confirm = True
            # check controller input
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == controllerKeys['x']:
                    self.confirm = True
                elif event.button == controllerKeys['circle']:
                    self.clearTextBox()
                
            


