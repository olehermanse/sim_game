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

class Color:
    def __init__(self, r,g,b,a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def rgba(self):
        return (self.r, self.g, self.b, self.a)

    def __getitem__(self, key):
        if type(key) is not int:
            raise TypeError
        return self.rgba()[key]

    colors = {
        "red":   (255,0,0,255),
        "green": (0,255,0,255),
        "blue":  (0,0,255,255),
        "white": (255,255,255,255),
        "black": (0,0,0,255)
    }

    @classmethod
    def get(cls, name):
        return Color(cls.colors[name])

class Renderer:
    @staticmethod
    def start(window):
        window.clear()
        pyglet.gl.glClearColor(255,255,255,255)

class GraphicsObject:
    def __init__(self, pos=(0,0)):
        GraphicsObject.set_pos(self, pos[0],pos[1])

    def set_pos(self, x,y):
        self.x = float(x)
        self.y = float(y)

    def move_pos(self, dx, dy):
        self.x += dx
        self.y += dy

    # Sub class must override this function for drawing to work
    def draw(self):
        raise NotImplementedError

    # Can replace draw(), more optimized:
    def batch_add(self, batch):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

#TODO: make colored rect separate class
class GraphicsRectangle(GraphicsObject):
    def __init__(self, width, height, fill=(128,128,128,255), stroke=(0,0,0,0), pos=(0,0), vel=(0,0), acc=(0,0), centered=False):
        self.stroke = Color(*stroke)
        self.fill = Color(*fill)
        self.centered = centered
        self.w = width
        self.h = height
        super().__init__(pos=pos)
        if centered:
            GraphicsRectangle.set_pos(self, pos[0], pos[1])

    def set_pos(self, x,y):
        super().set_pos(x,y)
        if self.centered:
            self.x -= self.w/2
            self.y -= self.h/2

    def set_fill(self, fill):
        self.fill = Color(*fill)

    def draw(self):
        pyglet.gl.glLineWidth(4)
        rect_vertices = pyglet.graphics.vertex_list(4,
            ('v2f', (self.x,        self.y) +
                    (self.x+self.w, self.y) +
                    (self.x+self.w, self.y+self.h) +
                    (self.x,        self.y+self.h)
            ),
            ('c4B', self.fill.rgba() * 4)
        )
        rect_vertices.draw(pyglet.gl.GL_QUADS)

        rect_vertices.colors = self.stroke.rgba() * 4
        rect_vertices.draw(pyglet.gl.GL_LINE_LOOP)


# =========================== NEW GRAPHICS MODULE ============================

class ColoredRectangle(Rectangle):
    def __init__(self, dimensions, *, pos=(0,0),  anchor=(0,0), offset=(0,0), fill=(255,0,0), stroke=(0,0,0)):
        super().__init__(pos=pos, dimensions=dimensions, offset=offset, anchor=anchor)
        self.stroke = Color(*stroke)
        self.fill = Color(*fill)
        self.enabled = True

    def set_fill(self, fill):
        self.fill = Color(*fill)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def draw(self):
        if not self.enabled:
            return
        pyglet.gl.glLineWidth(4)
        points = []
        for point in self.points():
            points += point.xy()
        rect_vertices = pyglet.graphics.vertex_list(4,
            ('v2f', points),
            ('c4B', self.fill.rgba() * 4)
        )
        rect_vertices.draw(pyglet.gl.GL_QUADS)

        rect_vertices.colors = self.stroke.rgba() * 4
        rect_vertices.draw(pyglet.gl.GL_LINE_LOOP)
