# from sound_midi import Midi
# from sound_pygame import Pygame_player
from sound_pyaudio import Wave
# from sound_lib import SoundLib
# import os
# import time

# format: (track,channel,instrument,pitch,time,duration,volume)

notes = [(0,0,27,90,0,0.1,50),
         (0,0,27,70,0.1,0.1,50),
         (0,0,27,80,0.2,0.1,50),
         (0,0,27,67,0.3,0.1,50),
         (0,0,27,40,0.4,0.1,50),
         (0,0,27,30,0.5,0.1,50),
         (0,0,27,90,0.6,0.1,50),
         (0,0,27,67,0.7,0.1,50)]

wave = Wave()
wave.play_notes(notes)
# midi = Midi()
# midi.midimaker(0,1,os.pardir + "/sounds",100,notes)
# robotid = 0
# path = ""
# file = ""
# pyplay = Pygame_player()
# sl = SoundLib()

#wave.play_notes_thread(notes)


# for file in os.listdir(os.pardir + "/sounds"):
#     if file.startswith(str(robotid)):
#         path = os.pardir + "/sounds/" + file
#         break

# print(path)
# print(file)
# duration = pyplay.extract_duration(file)
# print(duration)
# print(sl.midi_to_freq(100))
# print(sl.freq_to_midi(2600))

# pyplay.playsound(path,duration)
# time.sleep(duration)
