#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sound player using pygame"""

__author__    = ["Tor Jan Derek Berstad"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

try:
    from pygame import mixer
except:
    print("Could not import pygame")
import time
import threading

class Pygame_player:
    # Plays notes, do not run in main thread
    def playsoundthread(self, ident, duration):
        mixer.init()
        mixer.music.load(ident)
        mixer.music.play()
        time.sleep(duration)
        mixer.music.stop()

    # Gets the duration if the file uses the "id_duration.mid" naming convention.
    def extract_duration(self,ident):
        replaced = ident.replace('.','_')
        splt = replaced.split('_')
        return int(splt[1])

    # Calls the playsoundthread() function in a new thread.
    def playsound(self, ident, duration):
        try:
            t = threading.Thread(target=self.playsoundthread,args=(ident, duration))
            t.daemon = True
            t.start()
        except Exception as inst:
            print(type(inst))     # the exception instance
            print(inst.args)      # arguments stored in .args
            print(inst)            # __str__ allows args to be printed directly