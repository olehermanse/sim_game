#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim_game main class"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from graphics import SpriteObject, TextObject

class Game:
    def __init__(self, window):
        self.window = window
        #self.cat = SpriteObject('kitten.jpg', center=True, pos=(400,300), vel=(0,100), acc=(0,-100))
        self.message = TextObject("Hello, world", size=32, pos=(400,300), vel=(0,100), acc=(0,-100))

    def draw(self):
        self.window.clear()

        #self.cat.draw()
        self.message.draw()

    def update(self, dt):
        #self.cat.update(dt)
        self.message.update(dt)
