from fractions import Fraction
from music21 import midi, note, stream, instrument, meter, key
from math import fabs

# NOTEBOOK BASICS #################################

UNIT = 1 / 4  # durations expressed as UNIT * (whole note) (currently: quarter note)


def get_quarter_length():
    return UNIT


def percussion_hit(duration, pitch="C4"):
    # Create Note object for percussion hits (default pitch is C4)
    return note.Note(pitch, quarterLength=duration * (4 * UNIT))


def create_percussion(instru=instrument.Woodblock(), time_sig=None):
    # Initialize a percussion stream with Woodblock timbre
    # If time signature is None, no measure splits
    if time_sig is None:
        drum_part = stream.Measure()
    else:
        drum_part = stream.Stream()
        drum_part.timeSignature = meter.TimeSignature(time_sig)

    drum_part.insert(0, instru)
    return drum_part


def append_event(duration, original_stream, rest=False, pitch='C4'):
    # Returns a new_stream obtained by appending a rhythmical event or a rest of given duration to the original_stream
    new_stream = original_stream
    if rest:
        new_stream.append(note.Rest(quarterLength=duration * (4 * UNIT)))
    else:
        new_stream.append(percussion_hit(duration, pitch))
    return new_stream


def rhythm_from_sequence(durations, instru=instrument.Woodblock(), time_sig=None, pitch='C4', rhythm=None):
    # Generate rhythmic stream from a list of durations. Rests are indicated by specifying a duration as a string
    if rhythm is None:
        # pass an existing stream 'rhythm' to append the durations, otherwise a new one will be created
        rhythm = create_percussion(instru, time_sig)
    for dur in durations:
        is_rest = False
        if dur != 0:
            if dur < 0:
                # if duration is given as a string, interpret as rest and turn string into a numerical value
                is_rest = True
                dur = -dur

            rhythm = append_event(dur, rhythm, rest=is_rest, pitch=pitch)
    return rhythm


def play(score):
    # Shortcut to play a stream
    midi.realtime.StreamPlayer(score).play()


# OUR FUNCTIONS (insert the meme) #############################


def sequence_from_string_basic(string: str):
    """
    To use with chars: A, B, C, D, E, +, -
    A: half note
    B: quarter
    C: eighth
    D: sixteenth
    E: triplet
    +: extend previous duration by 50%
    -: divide previous duration by 2
    :param string: input string
    :return: sequence of durations
    """
    tab = []
    for c in string:
        if c == 'A':
            tab.append(2)
        elif c == 'B':
            tab.append(1)
        elif c == 'C':
            tab.append(1 / 2)
        elif c == 'D':
            tab.append(1 / 4)
        elif c == 'E':
            tab.append(1 / 3)
        elif c == '+':
            if len(tab) > 0:
                tab[-1] = tab[-1] + 0.5 * tab[-1]
        elif c == '-':
            if len(tab) > 0:
                tab[-1] = tab[-1] / 2
    return tab


def sequence_from_string_complex(string: str):
    """
    To use with chars: A, B, C, D, E, F, +, -, [, ]
    A: half note
    B: quarter
    C: eighth
    D: sixteenth
    E: triplet
    F: quintuplet
    +: add previous and next duration
    -: make previous note a rest (value: -1 * duration of rest)
    [: extend previous duration by 50%
    ]: divide previous duration by 2
    :param string: input string
    :return: sequence of durations
    """

    def char_to_duration(c: str, tb: list):
        if c == 'A':
            tb.append(2)
        elif c == 'B':
            tb.append(1)
        elif c == 'C':
            tb.append(1 / 2)
        elif c == 'D':
            tb.append(1 / 4)
        elif c == 'E':
            tb.append(1 / 3)
        elif c == 'F':
            tb.append(1 / 5)
        elif c == '[':
            if len(tb) > 0:
                tb[-1] = tb[-1] + 0.5 * tb[-1]
        elif c == ']':
            if len(tb) > 0:
                tb[-1] = tb[-1] / 2
        elif c == '-':
            if len(tb) > 0:
                tb[-1] = -tb[-1]
        return tb[-1]

    def is_duration_char(c: str):
        return c in ['A', 'B', 'C', 'D', 'E', 'F']

    str_arr = [c for c in string]
    tab = []
    while not len(str_arr) == 0:
        nb_chars_read = 1

        if str_arr[0] == '+' and len(str_arr) >= 2:
            nb_chars_read = 2
            if len(tab) > 0 and is_duration_char(str_arr[1]):
                old_read = tab[-1]
                new_read = char_to_duration(str_arr[1], tab)
                new_dur = fabs(old_read) + fabs(new_read)
                if old_read < 0:
                    new_dur = -new_dur
                tab[-2] = new_dur
                tab = tab[:-1]

        else:
            char_to_duration(str_arr[0], tab)

        str_arr = str_arr[nb_chars_read:]  # remove chars read
    return tab
