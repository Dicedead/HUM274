from L_system import *
from rhythm_toolkit import *
from L_sys_rules_depot import *
from melody_toolkit import *
from random import randint

string_res = run_complex_for(4)
# print(string_res)
sequence = sequence_from_string_complex(string_res)
rhythm = rhythm_from_sequence(sequence, instrument.Piano(), '4/4')
rhythm.write('midi', 'midi/complex_rhythm_treatment.midi')
print('Done!')


# some_length = len(sequence)
# part = combine_voices(some_length, sequence,[[randint(0, some_length) for i in range(some_length)] for j in range(2)])
# part.write('midi', 'midi/test_voices.midi')
# print("Done!")
