#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Library of general sound functions."""

__author__    = ["Tor Jan Derek Berstad"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

class SoundLib:
    def __init__(self, midi = None):
        if midi is None:
            self.midi = []
        a = 440
        for x in range (126):
            self.midi.append((a / 32) * (2**((x - 9)/12)))

    # Converts MIDI Note values to frequency
    def midi_to_freq(self, midi_n):
        return self.midi[midi_n]

    # Converts Frequency values to MIDI note values
    def freq_to_midi(self, freq):
        diffs = [abs(x - freq) for x in self.midi]
        min_value = min(diffs)
        return diffs.index(min_value)