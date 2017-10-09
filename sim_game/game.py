#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim_game main class"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from graphics import GraphicsRectangle, Renderer
from physics import SpriteObject, TextObject
from robot import Robot

import random

class World:
    def __init__(self, w, h):
        self.w, self.h = w, h

class Game:
    def __init__(self, window, w, h):
        self.window = window
        self.world = World(w,h)
        self.robots = []
        for _ in range(2):
            x = random.randint(50, w-50)
            y = random.randint(50, h-50)
            self.make_robot(x,y)

    def make_robot(self, x, y):
        if len(self.robots) > 10:
            return
        dna = None
        if len(self.robots) > 1:
            dna = self.robots[0].dna.combine(self.robots[1].dna)
        r = Robot(self.world, pos=(x,y), centered=True, dna=dna,
                  stroke=(0,0,0,255), fill=(128,128,128,255))
        self.robots.append(r)

    # TODO: change to batch drawing for performance
    def draw(self):
        Renderer.start(self.window)
        for r in self.robots:
            r.draw()

    def update(self, dt):
        for r in self.robots:
            r.update(dt)

    def mouse_motion(self, x, y, dx, dy):
        pass

    def mouse_press(self, x, y, button, modifiers):
        pass

    def mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.make_robot(x,y)

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
