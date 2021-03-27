from fractions import Fraction
from music21 import midi, note, stream, instrument, meter, key

# NOTEBOOK BASICS #################################

UNIT = 1/4  # durations expressed as UNIT * (whole note) (currently: quarter note)


def get_quarter_length():
    return UNIT


def percussion_hit(duration, pitch="C4"):
    # Create Note object for percussion hits (default pitch is C4)
    return note.Note(pitch, quarterLength=duration * (4 * UNIT))


def create_percussion(time_sig=None):
    # Initialize a percussion stream with Woodblock timbre
    # If time signature is None, no measure splits
    if time_sig is None:
        drum_part = stream.Measure()
    else:
        drum_part = stream.Stream()
        drum_part.timeSignature = meter.TimeSignature(time_sig)

    drum_part.insert(0, instrument.Woodblock())  # assign woosblock timbre
    return drum_part


def append_event(duration, original_stream, rest=False, pitch='C4'):
    # Returns a new_stream obtained by appending a rhythmical event or a rest of given duration to the original_stream
    new_stream = original_stream
    if rest:
        new_stream.append(note.Rest(quarterLength=duration * (4 * UNIT)))
    else:
        new_stream.append(percussion_hit(duration, pitch))
    return new_stream


def rhythm_from_sequence(durations, time_sig=None, pitch='C4', rhythm=None):
    # Generate rhythmic stream from a list of durations. Rests are indicated by specifying a duration as a string
    if rhythm is None:
        # pass an existing stream 'rhythm' to append the durations, otherwise a new one will be created
        rhythm = create_percussion(time_sig=time_sig)
    for dur in durations:
        is_rest = False
        if dur != 0:
            if isinstance(dur, str):
                # if duration is given as a string, interpret as rest and turn string into a numerical value
                is_rest = True
                dur = Fraction(dur)

            rhythm = append_event(dur, rhythm, rest=is_rest, pitch=pitch)
    return rhythm


def play(score):
    # Shortcut to play a stream
    midi.realtime.StreamPlayer(score).play()

# OUR FUNCTIONS (insert the meme) #############################


def sequence_from_string_abcde(string: str):
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
            tab.append(1/2)
        elif c == 'D':
            tab.append(1/4)
        elif c == 'E':
            tab.append(1/3)
        elif c == '+':
            if len(tab) > 0:
                tab[-1] = tab[-1] + 0.5 * tab[-1]
        elif c == '-':
            if len(tab) > 0:
                tab[-1] = tab[-1] / 2
    return tab


# TODO more complex string to duration: treat + and - as binary operators, [ and ] as unary

