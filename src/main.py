#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entry point and pyglet events"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from game import Game

try:
    import pyglet
    from pyglet.graphics import glScalef
except:
    print("Warning: could not import pyglet")

def update(dt):
    game.update(dt)

if __name__ == '__main__':
    window = pyglet.window.Window(800,600, resizable=True)
    game = Game(window)
    pyglet.clock.schedule_interval(update, 0.01)
    @window.event
    def on_draw():
        game.draw()

    @window.event
    def on_resize(width, height):
        print('The window was resized to {}x{}'.format(width, height))

    pyglet.app.run()
