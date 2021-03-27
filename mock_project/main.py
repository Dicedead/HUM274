from L_system import *
from rhythm_toolkit import *
from depot_ideas import *
from melody_toolkit import *
from random import randint

string_res = run_abcde_for(4)
sequence = sequence_from_string_abcde(string_res)

some_length = len(sequence)
part = combine_voices(some_length, sequence, [[randint(0, some_length) for i in range(some_length)] for j in range(2)])
part.write('midi', 'midi/test_voices.midi')
print("Done!")
