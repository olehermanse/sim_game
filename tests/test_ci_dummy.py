#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import path_fix

from sim_game import ci_dummy as ci
from sim_game.ci_dummy import double_a_number

def test_dummy_functions():
    assert ci.double_a_number(7) == 7*2
    assert double_a_number(7) == 7*2
