from harmonisation.melody_main import *
from l_system.rhythm_main import *
from harmonisation.melody_toolkit import *


def notes_array(tonality, bass, first_chord, length_composition):
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


if __name__ == "__main__":

    length_piece = 10
    voices = notes_array(Key.DO_MAJOR, bass_do_major, start_chord_do_major, length_piece)
    string_res = run_slow_for(4)
    sequence = sequence_from_string_slow(string_res)
    instruments = [instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()]

    parts = combine_voices(len(voices[0]), sequence, voices, inst=instruments, time_sig="3/4")

    parts.write('midi', 'midi' + platform_str + 'convergence_complexification_slow_2.mid')
