import math

import music21.stream

from l_system.rhythm_main import *
from harmonisation.melody_toolkit import *

"""
Thankfully, *Boléro*'s main rhythm is very easy and repetitive and can be cut down in to 3 parts A, B & C, organised in 
the sequence: ABAC. A groups the first 3 sextuplets and the following eighth note, B is a group of 3 sextuplets followed 
by 3 eighth notes, and C encompasses 9 sextuplets followed by a final eighth note. After some initial turbulence, 
the tail of the produced string becomes several repetitions of the ABAC motives. A, B & C are encoded as ``L-System`` 
rules in our code, with a twist: instead of sextuplets, sixteenth notes are used in A, turning the *Boléro*'s time 
signature into a 7/8. Then, the decision was later made to ease back into the *Boléro*'s 3/4, for reasons stated below.
"""

if __name__ == "__main__":
    bolero_rhythm = sequence_from_string_bolero(run_bolero_for(3, False))
    quarter_length = math.floor(len(bolero_rhythm)/4)
    bolero_rhythm = bolero_rhythm[:quarter_length] + bolero_rhythm[3 * quarter_length:]
    length = int(len(bolero_rhythm))
    bolero_score = combine_voices(length, bolero_rhythm, [[7 for _ in range(length)]], inst=[instrument.Woodblock()],
                                  time_sig="3/4")

    bolero_2_measures = music21.stream.Score()
    part_bolero_2_measures = music21.stream.Part(instrument=instrument.Woodblock(), time_sig="3/4")
    part_bolero_2_measures.append(note.Note(duration=dur.Duration(1/3)))

    bolero_score.write('midi', 'midi' + platform_str + 'convergence_bolero_sextuplet.mid')
