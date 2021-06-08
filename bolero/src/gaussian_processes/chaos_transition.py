from gaussian_processes.brownian_motion import brownian_motion
from gaussian_processes.metrical_structure import show_original
from util import *

# opening our midi file and putting it on a stream
mf = midi.MidiFile()
mf.open(f"media{platform_str}Bolero-Ravel_Loop.mid")
mf.read()
s1 = stream.Stream()
s1.append(midi.translate.midiFileToStream(mf))
mf.close()

# Note to which we converge : E4
E_PITCH = 64


def transition_to_chaos(s1, convergence_note=E_PITCH):
    """
    Takes a stream and makes it "transition to chaos"

    :param s: stream in which to introduce chaotic elements
    :convergence_note: note onto which to slowly converge
    :return:
    """
    # stream to accumulate the midi parts
    new_stream1 = stream.Stream()

    # time sig and tempo
    ts = meter.TimeSignature('3/4')
    new_stream1.append(tempo.MetronomeMark(number=72))
    new_stream1.insert(0, ts)

    # an instrument to play our score
    new_stream1.insert(0, instrument.Guitar())

    # getting the arrays of brownian motion (we create one dimension of brownian motion per track in the midi file)
    _, _, diff_brownian_motion = brownian_motion(dimensions=len(mf.tracks))

    # looping over the different parts
    for parts in s1:
        # and getting the corresponding brownian motion array (one per track/part)
        for part, single_brownian_motion in zip(parts, diff_brownian_motion.transpose()):

            # creating a part with the right Time signature
            new_part = stream.Part()
            new_part.insert(0, ts)

            # to shift the array on each iteration
            index = 0

            # looping five times on the same two measures
            for _ in range(5):
                for element in part.flat.notesAndRests:

                    # shifting the array
                    move = single_brownian_motion[index]
                    index += 1

                    # if the brownian motion goes up and the length is smaller than two (the length of a half-note)
                    # we increase the duration of the element so as to slowly remove rythmic values,
                    # all notes starting to play longer until the length of a half-note
                    elem_duration = element.duration.quarterLength
                    if (elem_duration < 2 and move >= 0):

                        new_elem_duration = round((elem_duration + move) * 4) / 4
                        element.duration = dur.Duration(quarterLength=new_elem_duration)

                    # if the brownian motion is more than -1, we add the element
                    # otherwise it is removed to make the listener lose their balence by violently and
                    # sporadically simplifying the rythm
                    elif move >= -1:

                        # if the element is a chord, no new modifications occur, we add it
                        if element.isClassOrSubclass((chord.Chord,)):
                            c = chord.Chord(element.notes, duration=element.duration)
                            new_part.append(c)
                        else:

                            # if the element is a rest, no new modifications occur, we add it
                            if element.name == 'rest':
                                r = note.Rest(duration=element.duration)
                                new_part.append(r)
                            else:

                                # if element is a note, we shift it's pitch towards E4 (convergence note)
                                elem_pitch = element.pitch.midi
                                to_add = 0
                                if elem_pitch < E_PITCH:
                                    to_add = 1
                                elif elem_pitch > E_PITCH:
                                    to_add = -1

                                element.pitch.midi = elem_pitch + to_add
                                n = note.Note(duration=element.duration, pitch=element.pitch)
                                new_part.append(n)

            # inserting the part
            new_stream1.insert(0, new_part)

    return new_stream1


if __name__ == "__main__":
    # Original score to compare with the new chaotic one
    show_original(s1)

    # Score after the introduction of chaotic elements
    stream_copy = stream.Stream(s1)
    new_stream1 = transition_to_chaos(stream_copy)
    new_stream1.show()

    play(new_stream1)

