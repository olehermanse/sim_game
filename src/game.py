#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim_game main class"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from graphics import SpriteObject, TextObject, Rectangle, Renderer
from robot import Robot

import random

class Game:
    def __init__(self, window):
        self.window = window
        self.robots = []
        for _ in range(4):
            x = random.randint(50,750)
            y = random.randint(50,550)
            r = Robot(pos=(x,y), stroke=(0,0,0,255), fill=(128,128,128,255),
                               centered=True)
            self.robots.append(r)

    # TODO: change to batch drawing for performance
    def draw(self):
        Renderer.start(self.window)
        for r in self.robots:
            r.draw()

    def update(self, dt):
        for r in self.robots:
            r.update(dt)
