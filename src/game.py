#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim_game main class"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

import os
import sys
import json
import pygame
from time import sleep
from pygame.locals import *


class color:
    black = (0,0,0)
    white = (255, 255, 255)

class Label:
    def __init__(self, text, font):
        self.text = font.render(text, True, color.black)
        self.rect = self.text.get_rect()

    def set_pos(self, x,y):
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self, surface):
        surface.blit(self.text, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600), 0, 32)
        self.font = pygame.font.SysFont(None, 48)
        pygame.display.set_caption('sim_game')
        self.message = Label("Hello, sim", self.font)
        self.message.set_pos(400,300)

    def draw(self):
        self.surface.fill(color.white)
        self.message.draw(self.surface)
        pygame.display.update()

    def run(self):
        while True:
            sleep(0.01)
            self.draw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    g = Game()
    g.run()
