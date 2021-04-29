from music21 import note, stream, duration, instrument
from harmonization import *
from L_sys_rules_depot import *


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


def combine_voices(length: int, rhythm, *voices, inst=None, time_sig='4/4'):
    """
    :param time_sig: well..
    :param inst: list of used instruments
    :param length: common length of voices to consider
    :param rhythm: rhythmic line: sequence of durations
    :param voices: sequences of integers encoding notes
    :return stream of chords
    """

    if inst is None:
        inst = [instrument.Piano()]
    voices = voices[0]
    score = stream.Score(timeSignature=time_sig)

    parts = [stream.Part() for _ in range(len(voices))]
    for part_index in range(len(voices)):
        for i in range(length):
            parts[part_index].append(translate(voices[part_index][i], rhythm[i]))

    for i in range(len(parts)):
        parts[i].insert(0, inst[i])
        score.insert(0, parts[i])

    return score


def select_path_in_tree(l_sys_string: str, char_list: list, length: int, composition_tree: Node):
    char_string = ""
    for c in l_sys_string:
        if c in char_list:
            char_string += c

    curr_node = composition_tree
    path = [curr_node.root]
    for i in range(length):
        if not isinstance(curr_node, Leaf) and len(curr_node.children) > 0:
            curr_node = curr_node.children[char_list.index(char_string[i]) % len(curr_node.children)]
            path.append(curr_node.root)
        elif isinstance(curr_node, Leaf):
            path.append(curr_node.root)
            break

    return path


if __name__ == '__main__':
    start_chord = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
    # bass_line = [DO, FA, SOL, SI, DO, DO, LA, FA, SOL, SOL, DO, FA, SOL, DO, DO]
    bass_line = [DO, FA, SOL, SI, DO, DO, LA]
    compositionTree = Node(start_chord, 1, [])

    compose(start_chord, bass_line[1:], compositionTree)
    print(compositionTree.level())
    print(to_arrays(select_path_in_tree(run_complex_for(4), chars_complex(), compositionTree)))
