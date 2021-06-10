import math

import music21.stream

from l_system.rhythm_main import *
from harmonisation.melody_toolkit import *


def notes_array(tonality, bass, first_chord, length_composition):
    """
    Construct 4 parts
    :param tonality: Desired tonality
    :param bass: Bass line in the tonality
    :param first_chord: First chord in the composition
    :param length_composition
    :return: array of 4 voices of notes
    """
    voices_arrays = [[], [], [], []]
    next_start_chord = first_chord
    for j in range(length_composition):
        next_compos_tree = Node(next_start_chord, 1, [])
        compose(next_start_chord, bass[1:], next_compos_tree, False, tonality)
        path = select_path_in_tree_harm(len(bass), next_compos_tree)
        next_start_chord = path[-1]
        path = to_arrays(path)
        for i in range(4):
            voices_arrays[i].extend(path[i])

    return voices_arrays


def combine_score_and_rhythm(curr_score: music21.stream.Score, curr_rhythm):
    """
    Combine a music21 Score and some rhythmic line
    :param curr_score: Rhythm-less harmonised notes
    :param curr_rhythm: Array of floats expressing durations
    :return: Complete score
    """
    new_score = music21.stream.Score()
    for curr_part in curr_score.parts:
        new_part = music21.stream.Part()
        for i in range(len(curr_part.notes)):
            new_part.append(note.Note(nameWithOctave=curr_part.notes[i].nameWithOctave,
                                      duration=dur.Duration(math.fabs(curr_rhythm[i]))))
        new_score.insert(0, new_part)
    return new_score

if __name__ == "__main__":

    voices = converter.parse('midi/input_midis/3_16.mid')
    string_res = run_complex_for(4)
    sequence = sequence_from_string_complex(string_res)
    instruments = [instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()]

    score_comp = combine_score_and_rhythm(voices, sequence)

    score_comp.write('midi', 'midi' + platform_str +
                     'convergence_complexification_complex_kept.mid')
