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
    print("Warning: could not import pyglet")

class GraphicsObject:
    def __init__(self, pos=(0,0), vel=(0,0), acc=(0,0)):
        self.set_pos(pos[0],pos[1])
        self.set_vel(vel[0],vel[1])
        self.set_acc(acc[0],acc[1])

    def set_pos(self, x,y):
        self.x = float(x)
        self.y = float(y)

    def set_vel(self, dx, dy):
        self.dx = float(dx)
        self.dy = float(dy)

    def set_acc(self, ddx, ddy):
        self.ddx = float(ddx)
        self.ddy = float(ddy)

    # Sub class must override this function for drawing to work
    def draw(self):
        raise NotImplementedError

    # Can replace draw(), more optimized:
    def batch_add(self, batch):
        raise NotImplementedError

    # Note: if you don't need acceleration and velocity
    #       simply call set_pos instead
    def update(self, dt):
        s = self
        dt = float(dt)
        # Do all calculations first (right side) then assign (left side):
        s.x, s.y, s.dx, s.dy = float(s.x  + dt*s.dx),\
                               float(s.y  + dt*s.dy),\
                               float(s.dx + dt*s.ddx),\
                               float(s.dy + dt*s.ddy)

class SpriteObject(GraphicsObject):
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

class TextObject(GraphicsObject):
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

class Rectangle(GraphicsObject):
    def __init__(self, width, height, fill=(0,0,255,255), stroke=(0,0,0,0), pos=(0,0), vel=(0,0), acc=(0,0)):
        super().__init__(pos=pos, vel=vel, acc=acc)
        self.w = width
        self.h = height
        self.stroke = stroke
        self.fill = fill

    def draw(self):
        rect_vertices = pyglet.graphics.vertex_list(4,
            ('v2f', (self.x,        self.y) +
                    (self.x+self.w, self.y) +
                    (self.x+self.w, self.y+self.h) +
                    (self.x,        self.y+self.h)
            ),
            ('c4B', self.fill * 4)
        )
        rect_vertices.draw(pyglet.gl.GL_QUADS)

        rect_vertices.colors = self.stroke * 4
        rect_vertices.draw(pyglet.gl.GL_LINE_LOOP)

    def update(self, dt):
        super().update(dt)
