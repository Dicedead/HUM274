from music21 import note, chord


def translate(int_note, duration):
    """
    Given an integer value of a note, get a corresponding music21.note object
    :param int_note: integer value of the note
    :param duration: duration of desired note
    :return music21.note
    """
    # TODO implement
    return note.Note('C4', duration=duration)


class Voice:

    def __init__(self, *notes: list):
        """
        Instantiate a Voice object: essentially an array of integers
        """
        self.notes = notes

    def append(self, note):
        self.notes.append(note)


def combine_voices(length: int, rhythm, *voices):
    """
    :param length: common length of voices to consider
    :param rhythm: rhythmic line: sequence of durations
    :param voices: sequences of integers encoding notes
    :return stream of chords
    """
    tab = []
    for i in range(length):
        tab.append(chord.Chord([translate(voice[i], rhythm[i]) for voice in voices]))
