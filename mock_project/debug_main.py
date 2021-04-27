from melody_toolkit import *
from custom_instruments import *
from new_harmonization import *


string_res = run_complex_for(4)


start_chord_c_major = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
bass_c_major = [DO, FA, SOL, SI, DO + OCTAVE, FA, LA, FA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]
start_chord = Chord(SOL, SI + 1 * OCTAVE, SOL + 2 * OCTAVE, RE + 3 * OCTAVE)
bass = [note + PERFECT_FIFTH_INTERVAL for note in bass_c_major]
tonality = Tonality.SOL_MAJOR

voices = [[], [], [], []]
compositionTree = Node(start_chord, 1, [])

compose(start_chord, bass[1:], compositionTree, tonality)
print(len(bass))
path = select_path_in_tree(string_res, chars_complex(), len(bass), compositionTree)
path = to_arrays(path)
print(len(path[0]))
for i in range(4):
    voices[i].extend(path[i])

parts = combine_voices(len(voices[0]), [], voices,
                       inst=[instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()])

parts.write('midi', 'midi/output_final.mid')
parts.show()
print("Done!")
