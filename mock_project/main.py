from L_system import *
from rhythm_toolkit import *
from depot_ideas import *

string_res = run_abcde_for(3)
sequence = sequence_from_string_abcde(string_res)
print(sequence)
rhythm = rhythm_from_sequence(sequence, '4/4')
# rhythm.show() # starts music21
rhythm.write('midi', 'midi/abcde.midi')

