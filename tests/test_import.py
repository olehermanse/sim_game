#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import path_fix

def test_import():
    from src import game
    from src import ci_dummy
    from src import main
    from src.ci_dummy import double_a_number
