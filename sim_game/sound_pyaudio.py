#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Midi generator using midiutil"""

__author__    = ["Tor Jan Derek Berstad"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

try:
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
except:
    print("Could not import pyaudio or Numpy")

import threading
import sim_game.sound_lib
import time

class Wave:

    def add_notes(self, notes):
        self.notes = notes

    #Play a notes array using pyaudio
    #Format: (track,channel,instrument,pitch,time,duration,volume)
    #TODO Test this
    def play_notes(self, notes=None):
        if not notes:
            notes = self.notes
        player = pyaudio.PyAudio()
        lib = sound_lib.SoundLib()
        fs = 44100  # sampling rate, Hz, must be integer
        stream = player.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=fs,
                             output=True)
        old = 0
        final = np.array([], dtype=np.float32)
        for note in notes:
            time.sleep(note[4]-old)
            duration = note[5]  # in seconds, may be float
            f = lib.midi_to_freq(note[3])  # sine frequency, Hz, may be float
            samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
            n = len(samples)
            level = (note[6])/100
            volume = [level]*n # range [0.0, 1.0]
            volume[0] = 0
            for index in range(1,n):
                volume[index] = (-(2*((index/n)-0.5))**6 + 1)*volume[index]
                samples[index] = samples[index]*volume[index]
            old = note[4] + duration
            final = np.append(final,samples)
        stream.write(final,num_frames=len(final))
        stream.stop_stream()
        stream.close()
        player.terminate()


    #Play notes in a new thread instead of in the main thread.
    def play_notes_thread(self, notes):
        try:
            self.add_notes(notes)
            t = threading.Thread(target=self.play_notes)
            t.start()
        except Exception as inst:
            print(type(inst))     # the exception instance
            print(inst.args)      # arguments stored in .args
            print(inst)            # __str__ allows args to be printed directly
