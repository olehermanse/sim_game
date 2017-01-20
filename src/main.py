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
    from pyglet.window import mouse
except:
    print("Warning: could not import pyglet")

def update(dt):
    game.update(dt)

if __name__ == '__main__':
    window = pyglet.window.Window(800,600, resizable=True)
    cursor = window.get_system_mouse_cursor("crosshair")
    window.set_mouse_cursor(cursor)
    game = Game(window)
    pyglet.clock.schedule_interval(update, 0.01)

    @window.event
    def on_draw():
        game.draw()

    @window.event
    def on_resize(width, height):
        print('The window was resized to {}x{}'.format(width, height))

    @window.event
    def on_mouse_motion(x,y,dx,dy):
        game.mouse_motion(x,y,dx,dy)

    def get_button(button):
        if type(button) is list:
            buttons = []
            for btn in button:
                buttons.append(get_button(btn))
            return btn
        if button == mouse.LEFT:
            return 1
        if button == mouse.RIGHT:
            return 2
        if button == mouse.MIDDLE:
            return 3

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        game.mouse_press(x, y, get_button(button), modifiers)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        game.mouse_release(x, y, get_button(button), modifiers)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        game.mouse_drag(x, y, dx, dy, get_button(buttons), modifiers)


    pyglet.app.run()
