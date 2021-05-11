from l_system.rhythm_main import *
from harmonisation.melody_toolkit import *

if __name__ == "__main__":
    bolero_rhythm = sequence_from_string_bolero(run_bolero_for(3, False))
    length = int(len(bolero_rhythm))
    bolero_score = combine_voices(length, bolero_rhythm, [[7 for _ in range(length)]], inst=[instrument.Woodblock()],
                                  time_sig="3/4")

    bolero_score.write('midi', 'midi' + platform_str + 'convergence_bolero.mid')
