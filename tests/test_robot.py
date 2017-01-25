#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import path_fix

from src import robot

# Do we get the expected error given the function call with arguments
def expect(error, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
        raise AssertionError
    except error:
        pass

# This test uses the RobotDNA object methods
# Can also be used as examples (documentation)
# Warning: test uses random (but *should* always pass)
def dna_methods():
    dna = robot.RobotDNA(randomize=True, size=0.7)
    assert dna.get("size") > 0.6

    dna.randomize()

    r = dna.get("red")
    dna.set(size=0.2, red=r, ratio=0.4)
    dna.set_bytes(red=255, green=0, blue=50, size=200)

    r,g,b,a = dna.get_color()
    dna.set_bytes(red=r, green=g, blue=b)
    dna.randomize()
    r,g,b,a = dna.get_color()
    dna.set_bytes(red=r, green=g, blue=b)

    s = dna.get_mapped_real("size", 0, 100)
    assert s >= 0 and s <= 100

def test_dna_methods():
    for _ in range(0,2000):
        dna_methods()

def test_key_error():
    expect(KeyError, robot.RobotDNA, none_key=True)
    expect(KeyError, robot.RobotDNA, none_key=0.5)
    dna = robot.RobotDNA()
    expect(KeyError, dna.get_byte, "fake_key")
    expect(KeyError, dna.set_byte, "superawesomegene", 1)
    expect(KeyError, dna.get, "fake_key")

def test_dna_bytes():
    dna = robot.RobotDNA()
    real_genes = dna["real"]
    # Don't add new genes to this list:
    expected_real_genes = ["red", "size", "ratio"]
    for key in expected_real_genes:
        assert key in real_genes
    for key in real_genes:
        for before in range(0,256):
            dna.set_byte(key, before)
            after = dna.get_byte(key)
            assert after == before
        # Test that invalid values raise exceptions:
        expect(ValueError, dna.set_byte, key, -1)
        expect(ValueError, dna.set_byte, key, 256)
