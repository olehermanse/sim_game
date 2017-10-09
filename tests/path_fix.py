#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Hacky way to make sure imports work'''
from os.path import abspath, dirname, realpath, join
import sys

# This allows imports to work, even if sim_game is not in python path:
package_location = abspath(join(dirname(realpath(__file__)) , ".."))
sys.path.insert(0, package_location)
