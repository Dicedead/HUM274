import random
from music21 import note, stream, duration, instrument
from harmonisation.harmonisation import *


def to_arrays(voices):
    """
    :param voices: list of chords
    """
    bass = []
    tenor = []
    alto = []
    soprano = []

    for tetrad in voices:
        bass.append(tetrad.b)
        tenor.append(tetrad.t)
        alto.append(tetrad.a)
        soprano.append(tetrad.s)

    return [bass, tenor, alto, soprano]


def combine_voices_harm(length: int, *voices, inst=None, time_sig='4/4'):
    """
    Combines the voices with music21 objects.
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
    """
    From a chord tree, randomly chooses a path (of an expected length)
    :param length: the expected length of the path
    :param composition_tree: the composition tree
    :return: the path
    """
    curr_node = composition_tree
    path = [curr_node.root]

    for i in range(length):

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

