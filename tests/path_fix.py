#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Hacky way to make sure imports work'''
import sys
import os

if os.path.exists("./sim_game/__init__.py"):
    sys.path.insert(0, "./")
if os.path.exists("../sim_game/__init__.py"):
    sys.path.insert(0, "../")
