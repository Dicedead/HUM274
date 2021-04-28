from debug_melody_toolkit import *
from custom_instruments import *
from new_harmonization import *


start_chord_do_major = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_do_major = [DO, FA, SOL, SI, DO + OCTAVE, FA, LA, FA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]
bass_do_major2 = [FA, LA, SI, DO, RE + OCTAVE, MI + OCTAVE, LA, SOL, SI, MI]

start_chord_sol_major = Chord(SOL, SI + 1 * OCTAVE, SOL + 2 * OCTAVE, RE + 3 * OCTAVE)
bass_sol_major = [note + PERFECT_FIFTH_INTERVAL for note in bass_do_major]

start_chord_la_minor = Chord(LA, DO + 2 * OCTAVE, LA + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_la_minor = [LA, RE, MI, SOL_S_LA_F, LA, RE, FA, RE, MI, SOL_S_LA_F, LA, RE, MI, LA, MI, LA]
bass_la_minor_debug_rule_7 = [LA, FA, MI, LA, MI, FA]

tonality = Tonality.LA_MINOR
start_chord = start_chord_la_minor
bass = bass_la_minor

voices = [[], [], [], []]
compositionTree = Node(start_chord, 1, [])

compose(start_chord, bass[1:], compositionTree, tonality)
print(compositionTree.level())
path = select_path_in_tree(len(bass), compositionTree)
path = to_arrays(path)[0:len(path)]
for i in range(4):
    voices[i].extend(path[i])

parts = combine_voices(len(voices[0]), [], voices,
                       inst=[instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()])

parts.write('midi', 'midi/output_final.mid')
parts.show()
print("Done!")
