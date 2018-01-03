#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim_game main class"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from sim_game.graphics import GraphicsRectangle, Renderer, ColoredRectangle
from sim_game.physics import SpriteObject, TextObject
from sim_game.robot import Robot

import random

class World:
    def __init__(self, w, h):
        self.w, self.h = w, h

class Game:
    def __init__(self, window, w, h):
        self.window = window
        self.world = World(w,h)
        self.robots = []
        self.init_robot_selector(w, h)

    def init_robot_selector(self, w, h):
        self.state = "baby_select"
        self.babies = []
        self.selectors = []
        self.selected = 1
        for i in range(3):
            x = w/2 - w/3 + i*w/3
            y = h/2
            baby = Robot(self.world, pos=(x,y))
            self.babies.append(baby)
            self.selectors.append(ColoredRectangle(pos=(x,y), dimensions=(w/4,h/2), fill=(200,200,200), stroke=(255,255,255)))

    def make_robot(self, x, y):
        if len(self.robots) > 10:
            return
        dna = None
        if len(self.robots) > 1:
            dna = self.robots[0].dna.combine(self.robots[1].dna)
        r = Robot(self.world, pos=(x,y), dna=dna)
        self.robots.append(r)

    # TODO: change to batch drawing for performance
    def draw(self):
        Renderer.start(self.window)
        if self.state == "baby_select":
            for r in self.selectors:
                r.draw()
            for r in self.babies:
                r.draw()
        else:
            for r in self.robots:
                r.draw()

    def update(self, dt):
        if self.state == "baby_select":
            for s in self.selectors:
                s.disable()
            self.selectors[self.selected].enable()
        else:
            for r in self.robots:
                r.update(dt)

    def mouse_motion(self, x, y, dx, dy):
        for index, sel in enumerate(self.selectors):
            if sel.contains_point((x,y)):
                self.selected = index

    def mouse_press(self, x, y, button, modifiers):
        pass

    def mouse_release(self, x, y, button, modifiers):
        if self.state == "baby_select":
            if button == 1:
                selected_baby = self.babies[self.selected]
                self.robots.append(self.babies[self.selected])
                selected_baby.sleep(2)
                self.babies = []
                self.state = "simulation"
        elif self.state == "simulation":
            if button == 1:
                self.make_robot(x,y)
        pass

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
