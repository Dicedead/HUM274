import random
from music21 import note, stream, duration, instrument
from new_harmonization import *


def translate(int_note, dur):
    """
    Given an integer value of a note, get a corresponding music21.note object
    :param int_note: integer value of the note
    :param dur: duration of desired note
    :return music21.note
    """
    first_char_arr = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    pitch = first_char_arr[int_note % 12] + str(int(2 + int_note / 12))

    if dur < 0:
        return note.Rest(duration=duration.Duration(quarterLength=-dur))
    return note.Note(pitch, duration=duration.Duration(quarterLength=dur))


def to_arrays(voices):
    """
    :param voices: list of chords
    """
    bass = []
    tenor = []
    alto = []
    soprano = []

    for chord in voices:
        bass.append(chord.b)
        tenor.append(chord.t)
        alto.append(chord.a)
        soprano.append(chord.s)

    return [bass, tenor, alto, soprano]


def combine_voices_harm(length: int, rhythm, *voices, inst=None, time_sig='4/4'):
    """
    :param length: common length of voices to consider
    :param voices: sequences of integers encoding notes
    :param inst: instruments
    :param time_sig: time signature
    :return stream of chords
    """

    voices = voices[0]
    if inst is None:
        inst = [instrument.BrassInstrument() if i % 2 == 0 else instrument.Piano() for i in range(len(voices))]
    score = stream.Score(timeSignature=time_sig)

    parts = [stream.Part() for _ in range(len(voices))]
    for part_index in range(len(voices)):
        for i in range(length):
            parts[part_index].append(translate(voices[part_index][i], 1))

    for i in reversed(range(len(parts))):
        parts[i].insert(0, inst[i])
        score.insert(0, parts[i])

    return score


def select_path_in_tree_harm(length: int, composition_tree: Node):
    curr_node = composition_tree
    path = [curr_node.root]

    for i in range(length):
        # FIXME: WHY LAST NODE AND THE FOLLOWING LEAF ARE THE SAME?

        if isinstance(curr_node, Node):
            list_index = list(range(0, len(curr_node.children)))
            random.shuffle(list_index)

            index = 0
            index_elem = list_index[index]

            while index < len(list_index) - 1 and curr_node.children[index_elem].total_depth() != length:
                index += 1
                index_elem = list_index[index]

            curr_node = curr_node.children[index_elem]
            path.append(curr_node.root)

    return path
