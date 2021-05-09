from math import fabs
from itertools import product
from enum import Enum
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (20, 3)
import scipy.io.wavfile
import numpy as np
from numpy.fft import rfftfreq, irfft
from numpy.random import normal
from IPython.display import Audio
import random
from scipy.io.wavfile import *
import librosa
from librosa import display
from music21 import midi, note, stream, instrument, meter, key, tempo, chord, duration
from music21 import duration as dur
from music21.note import Rest
import platform
from copy import deepcopy

platform_str = "\\" if platform.platform()[:7] == "Windows" else "/"


def play(score):
    # shortcut to play a music21 stream
    midi.realtime.StreamPlayer(score).play()


def translate(int_note, durat):
    """
    Given an integer value of a note, get a corresponding music21.note object
    :param int_note: integer value of the note
    :param durat: duration of desired note - if negative, interpret as rest
    :return music21.note
    """
    first_char_arr = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    pitch = first_char_arr[int_note % 12] + str(int(2 + int_note / 12))

    if durat < 0:
        return note.Rest(duration=duration.Duration(quarterLength=-durat))
    return note.Note(pitch, duration=duration.Duration(quarterLength=durat))
