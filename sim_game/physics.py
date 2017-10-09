#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""graphics primitives"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

try:
    import pyglet
    from pyglet.text import Label
    from pyglet.resource import image
except:
    print("Warning: could not import pyglet.")
    print("This is acceptable for tests, but rendering will not work.")

from sim_game.geometry import limit, Rectangle, Point
from sim_game.graphics import Color, Renderer, GraphicsObject, GraphicsRectangle

class PhysicsObject(GraphicsObject):
    def __init__(self, pos=(0,0), vel=(0,0), acc=(0,0), limits=None):
        GraphicsObject.set_pos(self, pos[0],pos[1])
        PhysicsObject.set_vel(self, vel[0],vel[1])
        PhysicsObject.set_acc(self, acc[0],acc[1])
        self.limits = limits

    def set_vel(self, dx, dy):
        self.dx = float(dx)
        self.dy = float(dy)

    def set_acc(self, ddx, ddy):
        self.ddx = float(ddx)
        self.ddy = float(ddy)

    def apply_limits(self):
        if not self.limits:
            return
        for var, lim in self.limits.items():
            self.__dict__[var] = limit(self.__dict__[var], *lim)


    # Note: if you don't need acceleration and velocity
    #       simply call set_pos instead
    def update(self, dt):
        self.apply_limits()
        s = self
        dt = float(dt)
        # Do all calculations first (right side) then assign (left side):
        x, y, dx, dy = float(s.x  + dt*s.dx),  \
                       float(s.y  + dt*s.dy),  \
                       float(s.dx + dt*s.ddx), \
                       float(s.dy + dt*s.ddy)
        # Sub classes can override these methods, like robot does:
        self.set_vel(dx,dy)
        self.set_pos(x,y)
        self.apply_limits()

# TODO: Make this inherit from Rectangle
class SpriteObject(PhysicsObject):
    def __init__(self, path, pos=(0,0), vel=(0,0), acc=(0,0), center=False):
        super().__init__(pos, vel, acc)
        self.image = image(path)
        self.width, self.height = self.image.width, self.image.height
        self.center = center

    def draw(self):
        if self.center:
            self.image.blit(self.x-self.width/2, self.y-self.height/2)
        else:
            self.image.blit(self.x, self.y)

class TextObject(PhysicsObject):
    def __init__(self, text, size, pos=(0,0), vel=(0,0), acc=(0,0)):
        self.label = Label(text, font_name="Arial", font_size=size,
                                 x=pos[0], y=pos[1],
                                 anchor_x="center", anchor_y="center")
        super().__init__(pos=pos, vel=vel, acc=acc)

    def draw(self):
        self.label.draw()

    def update(self, dt):
        super().update(dt)
        self.label.x = self.x
        self.label.y = self.y

class PhysicsRectangle(GraphicsRectangle, PhysicsObject):
    def __init__(self, width, height, **kwargs):
        """
        super init chain like this:
        PhysicsRectangle->Rectangle->PhysicsObject->GraphicsObject
        """
        GraphicsRectangle.__init__(self, width, height, **kwargs)

    def update(self, dt):
        super().update(dt)
