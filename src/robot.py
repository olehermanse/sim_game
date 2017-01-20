#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""graphics primitives"""

__author__   = ["Ole Herman Schumacher Elgesem", "Tor Jan Derek Berstad"]
__license__  = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from graphics import PhysicsRectangle, Rectangle
from collections import UserDict
import random

class RobotDNA(UserDict):
    def __init__(self, randomize=True, **kwargs):
        self.binary = {  # Binary, true or false genes

        }
        self.real = {    # Real valued genes
            "red": 0.5,
            "green": 0.5,
            "blue": 0.5,
            "size": 0.5,
            "ratio": 0.5
        }
        if randomize:
            self.randomize()
        self.set(**kwargs)

        self.master = {"binary": self.binary, "real": self.real}
        super().__init__(self.master)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if type(value) is bool:
                if key in self.binary:
                    self.binary[key] = value
                else:
                    raise KeyError
            else:
                if key in self.real:
                    assert value >= 0 and value <= 1
                    self.real[key] = float(value)
                else:
                    raise KeyError

    def get(self, key):
        # Returns a value or raises KeyError:
        if key not in self.binary:
            return self.real[key]
        if key not in self.real:
            return self.binary[key]

        # key in both dicts:
        raise RuntimeError

    def get_byte(self, key):
        val = int(self.real[key]*255.99)
        assert val < 256 and val >= 0
        return val

    def set_byte(self, key, val):
        if val >= 256 or val < 0:
            raise ValueError
        if key not in self.real:
            raise KeyError
        self.real[key] = val/255.99

    def set_bytes(self, **kwargs):
        for key, value in kwargs.items():
            if type(value) is bool:
                raise ValueError
            else:
                self.set_byte(key, value)

    def get_color(self):
        return (
            self.get_byte("red"),
            self.get_byte("green"),
            self.get_byte("blue"),
            255
        )

    def randomize(self):
        for key in self.binary:
            self.binary[key] = (random.random() >= 0.5)
        for key in self.real:
            self.real[key] = random.random()

    def get_mapped_real(self, key, start, stop):
        return ((stop-start)*self.real[key] + start)

# TODO: Separate out a cluster object class for multiple rect objects like this
class Robot(PhysicsRectangle):
    def __init__(self, *args, stroke=(0,0,0,255), fill=(128,128,128,255), **kwargs):
        self.dna = RobotDNA()
        ratio = (1/2**(self.dna.get_mapped_real("ratio",-1,1)))
        width = self.dna.get_mapped_real("size",50,100)
        height = width*ratio
        super().__init__(width, height, *args, **kwargs)
        self.body = Rectangle(width/3, height/3, *args, **kwargs)
        self.head = Rectangle(width*0.8, height*0.8, *args, **kwargs)
        self.head.move_pos(0,height/2)
        self.head.fill = self.dna.get_color()
        self.eye = Rectangle(width*0.6, height*0.2, *args, **kwargs)
        self.eye.set_fill((0,255,0,255))
        self.eye.move_pos(0,height/2+height/6)
        self.body_parts = [self.body, self.head, self.eye]

    def set_pos(self, x,y):
        dx = x - self.x
        dy = y - self.y
        self.move_pos(dx,dy)

    def set_vel(self, dx, dy):
        super().set_vel(dx,dy)
        # for part in self.body_parts:
        #     part.set_vel(dx,dy)

    def set_acc(self, ddx, ddy):
        super().set_acc(ddx,ddy)
        # for part in self.body_parts:
        #     part.set_acc(ddx,ddy)

    def move_pos(self, dx, dy):
        super().move_pos(dx,dy)
        for part in self.body_parts:
            part.move_pos(dx,dy)

    def draw(self):
        for part in self.body_parts:
            part.draw()

    def update(self, dt):
        self.ddx += random.uniform(-0.5, 0.5)
        self.ddy += random.uniform(-0.5, 0.5)
        super().update(dt)

        # for part in self.body_parts:
        #     part.set_acc(self.ddx, self.ddy)
        #     part.update(dt)
