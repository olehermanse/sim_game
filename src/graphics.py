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

class Color:
    colors = {
        "red":   (255,0,0,255),
        "green": (0,255,0,255),
        "blue":  (0,0,255,255),
        "white": (255,255,255,255),
        "black": (0,0,0,255)
    }
    @classmethod
    def get(cls, name):
        return cls.colors[name]

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

    def chain_print(self):
        return "GraphicsObject"

class PhysicsObject(GraphicsObject):
    def __init__(self, pos=(0,0), vel=(0,0), acc=(0,0)):
        GraphicsObject.set_pos(self, pos[0],pos[1])
        PhysicsObject.set_vel(self, vel[0],vel[1])
        PhysicsObject.set_acc(self, acc[0],acc[1])

    def set_vel(self, dx, dy):
        self.dx = float(dx)
        self.dy = float(dy)

    def set_acc(self, ddx, ddy):
        self.ddx = float(ddx)
        self.ddy = float(ddy)

    # Note: if you don't need acceleration and velocity
    #       simply call set_pos instead
    def update(self, dt):
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

    def chain_print(self):
        return "PhysicsObject->" + super().chain_print()

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

#TODO: make colored rect separate class
class Rectangle(GraphicsObject):
    def __init__(self, width, height, fill=(128,128,128,255), stroke=(0,0,0,0), pos=(0,0), vel=(0,0), acc=(0,0), centered=False):
        self.centered = centered
        self.w = width
        self.h = height
        super().__init__(pos=pos)
        if centered:
            Rectangle.set_pos(self, pos[0], pos[1])
        self.stroke = stroke
        self.fill = fill

    def set_pos(self, x,y):
        super().set_pos(x,y)
        if self.centered:
            self.x -= self.w/2
            self.y -= self.h/2

    def set_fill(self, fill):
        self.fill = fill

    def draw(self):
        pyglet.gl.glLineWidth(4)
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

    def chain_print(self):
        return "Rectangle->" + super().chain_print()

class PhysicsRectangle(Rectangle, PhysicsObject):
    def __init__(self, width, height, **kwargs):
        """
        super init chain like this:
        PhysicsRectangle->Rectangle->PhysicsObject->GraphicsObject
        """
        Rectangle.__init__(self, width, height, **kwargs)

    def update(self, dt):
        super().update(dt)

    def chain_print(self):
        return "PhysicsRectangle->" + super().chain_print()
