#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""graphics primitives"""

__author__   = ["Ole Herman Schumacher Elgesem", "Tor Jan Derek Berstad"]
__license__  = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'
try:
    from pyglet.media import Player
    from pyglet.media.procedural import Silence, Sine, Saw
except:
    print("Warning: could not import pyglet.")
    print("This is acceptable for tests, but rendering will not work.")

from graphics import PhysicsRectangle, GraphicsRectangle
from collections import UserDict
import random
import math

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

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

    def combine(self, dna, probability_average=0.3, weighted_average=True):
        parents = [self, dna]
        child = RobotDNA(randomize=False)
        for key in dna.binary:
            r = random.randint(0,1)
            child.binary[key] = parents[r].binary[key]

        for key in dna.real:
            p = random.uniform(0.0,1.0)
            if p < probability_average:
                w1 = 0.5
                if weighted_average:
                    w1 = random.uniform(0.0,1.0)
                w2 = 1.0 - w1
                a,b = parents[0].real[key], parents[1].real[key]
                child.real[key] = a * w1 + b * w2
            else:
                r = random.randint(0,1)
                child.real[key] = parents[r].real[key]
        return child


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
    def __init__(self, world, *args, stroke=(0,0,0,255), fill=(128,128,128,255),dna=None, **kwargs):
        if not dna:
            self.dna = RobotDNA()
        else:
            self.dna = dna
        self.world = world
        ratio = (1/2**(self.dna.get_mapped_real("ratio",-1,1)))
        width = self.dna.get_mapped_real("size",50,100)
        height = width*ratio
        super().__init__(width, height, *args, **kwargs)
        self.body = GraphicsRectangle(width/3, height/3, *args, **kwargs)
        self.head = GraphicsRectangle(width*0.8, height*0.8, *args, **kwargs)
        self.head.fill = self.dna.get_color()
        self.eye = GraphicsRectangle(width*0.6, height*0.2, *args, **kwargs)
        self.eye.set_fill((0,255,0,255))
        self.body_parts = [self.body, self.head, self.eye]
        self.targetx = random.uniform(0, self.world.w)
        self.targety = random.uniform(0, self.world.h)
        self.limits = None
        self.sleep_counter = 0.0
        self.sleeping = False

        p = Player()
        n = [261.6, 293.7, 329.7, 349.2, 392, 440, 493, 523.3, 587.4]
        l = len(n)
        for _ in range(5):
            # TODO: add envelope fading
            #       pyglet 1.3.0 will add support for envelopes
            s = Sine(0.1, n[random.randint(0,l-1)])
            p.volume = 0.25
            p.queue(s)
        p.play()

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

        self.body.set_pos(self.x, self.y)
        self.head.set_pos(self.x,self.y+self.h/2)
        self.eye.set_pos(self.x,self.y+self.h/2+self.h/6)

    def draw(self):
        for part in self.body_parts:
            part.draw()

    def sleep(self, t):
        self.sleeping = True
        self.sleep_counter = t
        self.eye.set_fill((0,0,255,255))

    def sleep_tick(self, dt):
        self.sleep_counter -= dt
        if self.sleep_counter > 0:
            self.sleeping = True
            return
        self.sleeping = False

    def sleep_update(self, dt):
        self.sleep_tick(dt)
        self.set_vel(0,0)
        self.set_acc(0,0)
        if not self.sleeping:
            self.eye.set_fill((0,255,0,255))
        super().update(dt)

    def update(self, dt):
        if self.sleeping:
            self.sleep_update(dt)
            return

        dx, dy = self.targetx - self.x,\
                 self.targety - self.y
        d = math.sqrt(dx**2 + dy**2)

        vel = 5 + 4*d + 0.02*d**2
        if vel>100:
            vel = 200
        self.dx, self.dy = vel * dx/d,\
                           vel * dy/d
        super().update(dt)

        while distance(self.targetx, self.targety, self.x, self.y) < 2:
            self.targetx = random.uniform(50,750)
            self.targety = random.uniform(50,550)
            self.sleep(random.uniform(1.0, 7.0))
