from util import *


def intro_metrical_structure(s):
    """
    Introduces the melodic theme (here of the Bolero) by gradually adding notes following the metrical structure
    :param s:
    :return: the new stream created
    """
    # stream to accumulate the midi parts
    new_stream = stream.Stream()

    # time sig and tempo
    ts = meter.TimeSignature('3/4')
    new_stream.append(tempo.MetronomeMark(number=72))
    new_stream.insert(0, ts)

    # an instrument to play our score
    new_stream.insert(0, instrument.Guitar())

    # probabilities for each of the beats of the measure to be added (metrical structure)
    initial_probabilities = np.array([3, 1, 2, 1, 2, 1], dtype='float32') / 10

    # looping over the different parts of the score
    for parts in s:
        for part in parts:

            # accumulator for the duration of the notes encountered
            durat = 0

            # creating a part with the right Time signature
            new_part = stream.Part()
            new_part.insert(0, ts)

            # reseting the probabilities for each part
            probabilities = deepcopy(initial_probabilities)

            # on each note or rest
            for element in part.flat.notesAndRests[0:100]:

                # increasing the probabilities once each two measures to create a sense
                # of convergence (the melody begins to make sense)
                elem_duration = element.duration.quarterLength
                if durat + elem_duration >= 6:
                    probabilities *= 1.6

                # getting the new accumulated duration
                durat = (durat + elem_duration) % 6

                # adding the current note with a particular probability
                # or substituting it by a rest of same duration
                if random.random() < probabilities[int(durat)] * elem_duration:
                    new_part.append(element)
                else:
                    r = note.Rest()
                    r.duration = element.duration
                    new_part.append(r)

            # inserting the part
            new_stream.insert(0, new_part)
    return new_stream


# showing (a part of) the original partition before using the intro_metrical_structures (to compare)
def show_original(s):
    original = stream.Stream()
    for parts in s:
        for part in parts:
            new_part = stream.Part()
            for element in part.flat.notesAndRests[0:100]:
                new_part.append(element)
            original.insert(0, new_part)
    original.show()

if __name__ == "__main__":
    # opening our midi file and putting it on a stream
    mf = midi.MidiFile()
    mf.open(f"media{platform_str}Bolero-Ravel_Flute_Bat_Strings.mid")
    mf.read()
    s = stream.Stream()
    s.append(midi.translate.midiFileToStream(mf))
    mf.close()
    show_original(s)

    # the new partition in which we gradually add more and more notes from the original partition
    new_stream = intro_metrical_structure(s)
    new_stream.show()

    play(new_stream)
