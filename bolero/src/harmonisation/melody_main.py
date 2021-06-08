from harmonisation.melody_toolkit import *
from harmonisation.harmonisation import *
from music21 import converter


# Do M
start_chord_3 = Chord(DO + OCTAVE, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_3 = [DO, FA, SOL, DO, LA, RE, SOL, SI, DO + OCTAVE]

# Sol M
start_chord_4 = Chord(RE + OCTAVE, LA + 1 * OCTAVE, RE + 2 * OCTAVE, FA_S_SOL_F + 2 * OCTAVE)
bass_4 = [RE, SOL, DO, RE, SOL, DO, RE, SI, MI, SOL, MI]

# Mi m
start_chord_5 = Chord(MI, SI + 1 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_5 = [MI, SI, MI, SOL, FA_S_SOL_F, SI, MI]

# La M
start_chord_6 = Chord(MI, SOL_S_LA_F + 1 * OCTAVE, SI + 1 * OCTAVE, MI + 2 * OCTAVE)
bass_6 = [MI, LA, RE, MI, LA, SOL_S_LA_F, LA, SI, MI, LA, SI]

# Mi M
start_chord_7 = Chord(SI, FA_S_SOL_F + 1 * OCTAVE, RE_S_MI_F + 2 * OCTAVE, SI + 2 * OCTAVE)
bass_7 = [SI, MI, LA, SI, MI, DO_S_RE_F, FA_S_SOL_F, SI, MI, SOL_S_LA_F]

# Do # m
start_chord_8 = Chord(SOL_S_LA_F, RE_S_MI_F + 1 * OCTAVE, DO + 2 * OCTAVE, SOL_S_LA_F + 2 * OCTAVE)
bass_8 = [SOL_S_LA_F, DO_S_RE_F + 1 * OCTAVE, SOL_S_LA_F, DO_S_RE_F + 1 * OCTAVE, RE_S_MI_F + 1 * OCTAVE, DO + 1 * OCTAVE, DO_S_RE_F + 1 * OCTAVE]

# Re b M
start_chord_9 = Chord(DO_S_RE_F + 1 * OCTAVE, FA + 2 * OCTAVE, DO_S_RE_F + 3 * OCTAVE, SOL_S_LA_F + 3 * OCTAVE)
bass_9 = [DO_S_RE_F + 1 * OCTAVE, SOL_S_LA_F, DO_S_RE_F + 1 * OCTAVE, LA_S_SI_F, FA_S_SOL_F, SOL_S_LA_F, LA_S_SI_F, DO_S_RE_F + 1 * OCTAVE, RE_S_MI_F + 1 * OCTAVE]

# La b m
start_chord_10 = Chord(SOL_S_LA_F, DO + 2 * OCTAVE, SOL_S_LA_F + 2 * OCTAVE, RE_S_MI_F + 3 * OCTAVE)
bass_10 = [SOL_S_LA_F, DO_S_RE_F, RE_S_MI_F, SOL_S_LA_F, DO_S_RE_F]

# Do b M
start_chord_11 = Chord(FA_S_SOL_F, DO_S_RE_F + 2 * OCTAVE, LA_S_SI_F + 2 * OCTAVE, FA_S_SOL_F + 3 * OCTAVE)
bass_11 = [SOL_S_LA_F, SI + OCTAVE, MI + OCTAVE]

# Fa b M
start_chord_12 = Chord(MI + OCTAVE, SI + OCTAVE, SOL_S_LA_F + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_12 = [MI, SI + OCTAVE, MI]

# Mi M
start_chord_13 = Chord(MI, SI + OCTAVE, SOL_S_LA_F + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_13 = [MI, LA, SI, MI, SI, MI]

# la m
start_chord_14 = Chord(LA, DO + 2 * OCTAVE, LA + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_14 = [LA, MI, LA, RE + OCTAVE, MI + OCTAVE, LA]

# Do M
start_chord_15 = Chord(DO + OCTAVE, MI + 2 * OCTAVE, DO + 3 * OCTAVE, SOL + 3 * OCTAVE)
bass_15 = [DO + OCTAVE, FA + OCTAVE, SI, MI + OCTAVE, LA]



def create_composition(key, start_chord, bass):
    voices = [[], [], [], []]
    composition_tree = Node(start_chord, 1, [])

    compose(start_chord, bass[1:], composition_tree, False, key)
    print(composition_tree)
    print("composition_tree's level (total number of different compositions) : " + str(composition_tree.level()))

    path = select_path_in_tree_harm(len(bass), composition_tree)
    # path = to_arrays(path)[0:len(path)]
    path = to_arrays(path)
    for i in range(4):
        voices[i].extend(path[i])

    parts = combine_voices_harm(len(voices[0]), voices,
                                inst=[instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()])

    parts.write('midi', 'midi/output_final.mid')
    parts.show()
    return parts


def concatenate_midi(midi1, midi2):
    part1 = converter.parse(midi1)
    part2 = converter.parse(midi2)

    for i in range(len(part1)):
        part1[i].append(part2[i])
    return part1


if __name__ == "__main__":
    create_composition(Key.DO_MAJOR, start_chord_15, bass_15)
    # parts = concatenate_midi('midi/121314.mid', 'midi/1516.mid')
    # parts.write('midi', 'midi/12_16.mid')
    # parts.show()
