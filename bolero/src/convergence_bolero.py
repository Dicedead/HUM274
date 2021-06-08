import math

import music21.stream

from l_system.rhythm_main import *
from harmonisation.melody_toolkit import *

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
