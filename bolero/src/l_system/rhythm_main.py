from l_system_data import *


def combine_voices(length: int, rhythm, *voices, inst=None, time_sig='4/4'):
    """
    Define a voice to be a sequence of integers encoding pitches.
    This function takes multiple voices + an array of note durations (the parameter: rhythm)
    It then superposes all the voices and creates a set of synchronous notes (could be one, two [interval],
    three to nine [chord], or more) and plays these sets consecutively according to the rhythm sequence

    Otherwise said, it adds the same rhythmical durations to each voice, causing them to be superposed

    :param time_sig
    :param inst: list of used instruments
    :param length: common length of voices to consider
    :param rhythm: rhythmic line: sequence of durations
    :param voices: sequences of integers encoding notes
    :return stream of chords
    """

    if inst is None:
        inst = [instrument.Piano()]
    voices = voices[0]
    score = stream.Score()
    score.timeSignature = meter.TimeSignature(time_sig)

    parts = [stream.Part() for _ in range(len(voices))]
    for part_index in range(len(voices)):
        parts[part_index].timeSignature = meter.TimeSignature(time_sig)
        for i in range(length):
            parts[part_index].append(translate(voices[part_index][i], rhythm[i]))

    for i in range(len(parts)):
        parts[i].insert(0, inst[i])
        score.insert(0, parts[i])

    return score


rhythm = sequence_from_string_complex(run_complex_for(4))
length = int(len(rhythm) / 60)
print(f"{length} notes kept")
score = combine_voices(length, rhythm, [[7 for i in range(length)]], inst=None, time_sig="3/4")

bolero_rhythm = run_bolero_for(3, True)
print(f"end of the sequence: {bolero_rhythm[-60:]}")

bolero_rhythm = sequence_from_string_bolero(run_bolero_for(3, False))
length = int(len(bolero_rhythm))
bolero_score = combine_voices(length, bolero_rhythm, [[7 for _ in range(length)]], inst=[instrument.Woodblock()],
                              time_sig="3/4")
bolero_score.show()
play(bolero_score)
