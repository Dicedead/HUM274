from L_system import *
from rhythm_toolkit import *
from L_sys_rules_depot import *
from melody_toolkit import *
from random import randint
from custom_instruments import *
from harmonization import *
from random import randint
import sys

string_res = run_complex_for(4)
# print(string_res)
sequence = sequence_from_string_complex(string_res)

start_chord = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
bass1 = [DO, FA, SOL, SI, DO + OCTAVE, FA, LA, FA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]
bass2 = [DO, RE, MI, DO, SOL, DO, FA, LA, SI, DO+OCTAVE, DO, MI, FA, SOL, SI, DO+OCTAVE]
bass3 = [DO, FA, LA, DO, RE, LA, SI, DO+OCTAVE, FA, DO, SOL, DO+OCTAVE, SI, DO+OCTAVE, SOL, DO+OCTAVE]
bass4 = [DO, SOL, SI, DO+OCTAVE, FA, SOL, DO+OCTAVE, LA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]

basses = [bass1, bass2, bass3, bass4]
assert len(basses[0]) == len(basses[1]) and len(basses[1]) == len(basses[2]) and len(basses[2]) == len(basses[3])



length_piece = 45

sys.stdout.write("[%s]" % (" " * length_piece))
sys.stdout.flush()
sys.stdout.write("\b" * (length_piece+1)) # return to start of line, after '['

next_start_chord = start_chord
voices = [[], [], [], []]
for j in range(length_piece):
    sys.stdout.write("-")
    sys.stdout.flush()

    next_compos_tree = Node(next_start_chord, 1, [])
    compose(next_start_chord, basses[randint(0, 3)][1:], next_compos_tree)
    path = select_path_in_tree(string_res, chars_complex(), len(basses[0]), next_compos_tree)
    next_start_chord = path[-1]
    path = to_arrays(path)
    for i in range(4):
        voices[i].extend(path[i])

sys.stdout.write("]\n")

parts = combine_voices(len(voices[0]), sequence, voices,
                       inst=[instrument.Piano(), instrument.Piano(), instrument.Accordion(), instrument.Violin()])

parts.write('midi', 'midi/output_final.mid')
# parts.show()
print("Done!")
