#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Robot DNA"""

__author__   = ["Ole Herman Schumacher Elgesem", "Tor Jan Derek Berstad"]
__license__  = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from collections import UserDict
import random

class DNA(UserDict):
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
        child = DNA(randomize=False)
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
