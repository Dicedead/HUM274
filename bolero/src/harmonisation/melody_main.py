from melody_toolkit import *

bass_do_major = [DO, FA, SOL, SI, DO + OCTAVE, FA, LA, FA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]
bass_sol_major = [note + PERFECT_FIFTH_INTERVAL for note in bass_do_major]
bass_la_minor = [LA, FA, MI, LA, RE, LA, MI, FA, MI, LA, SOL_S_LA_F, LA, FA, SI, MI, LA]

start_chord_sol_major = Chord(SOL, SI + 1 * OCTAVE, SOL + 2 * OCTAVE, RE + 3 * OCTAVE)
start_chord_la_minor = Chord(LA, LA + 1 * OCTAVE, MI + 2 * OCTAVE, DO + 3 * OCTAVE)


def create_composition(key, start_chord, bass):
    voices = [[], [], [], []]
    composition_tree = Node(start_chord, 1, [])

    compose(start_chord, bass[1:], composition_tree, False, key)
    # print(composition_tree)
    print("composition_tree's level (total number of different compositions) : " + str(composition_tree.level()))

    path = select_path_in_tree_harm(len(bass), composition_tree)
    path = to_arrays(path)[0:len(path)]
    for i in range(4):
        voices[i].extend(path[i])

    parts = combine_voices_harm(len(voices[0]), [], voices,
                                inst=[instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()])

    return parts

parts_1 = create_composition(Key.SOL_MAJOR, start_chord_sol_major, bass_sol_major)
parts_1.show()
play(parts_1)
