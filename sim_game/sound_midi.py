#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Midi generator using midiutil"""

__author__    = ["Tor Jan Derek Berstad"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

try:
    from midiutil.MidiFile import MIDIFile
except:
    print("Coould not find MIDIUtil")
import os
import math
import errno

class Midi:
    # Creates a folder if it does not exist.
    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # Generates a midi file with notes passed through the "notes" list, expects a list of 7-long tuples, with the
    # following format: (track,channel,instrument,pitch,time,duration,volume)
    def midimaker(self, id, noTracks,directory, tempo, notes):
        sound = MIDIFile(noTracks, adjust_origin=True)
        totalDuration = 0
        for i in range(noTracks):
            sound.addTrackName(i, 0, "track" + str(i))
            sound.addTempo(i,0,tempo)
        for note in notes:
            trackno = note[0]
            channel = note[1]
            instrument = note[2]
            pitch = note[3]
            time = note[4]
            duration = note[5]
            volume = note[6]
            sound.addNote(trackno, channel, pitch, time, duration, volume)
            sound.addProgramChange(trackno,channel,time,instrument)
            if((time + duration) > totalDuration):
                totalDuration += (time+duration-totalDuration)
        self.make_sure_path_exists(directory)
        binfile = open(directory + "/" + str(id) + '_' + str(math.ceil(totalDuration)) + '.mid', 'wb')
        sound.writeFile(binfile)
        return binfile.close()

    #Convert a MIDI file to a notes array
    #TODO Finish this.
    def midi_to_notes(self, id):
        notes = 0
        return notes
