"""
For the sake of simplicity, we will restrict ourselves to a simple harmonisation, with some assumptions:

The key will be C Major.
Each note of the bass line represents its corresponding grade in the key, hence each chord is in fundamental state,
i.e. there are no inversions.
The chords are only formed with fifths, i.e., we do not use seventh or ninth chords.

For the final project, we could implement a much more complex algorithm and objects in order to achieve a bigger variety
of better harmonizations: we could establish less assumptions and add more rules
"""

import itertools

DO = 0
RE = 2
MI = 4
FA = 5
SOL = 7
LA = 9
SI = 11
OCTAVE = 12

EPSILON = 7  # allowed delta between two notes when looking for a transition


class SimplifiedChord:
    def __init__(self, fundamental: int, third: int, fifth: int):
        self.fundamental = fundamental
        self.third = third
        self.fifth = fifth

    def includes(self, note: int):
        new_note = note % 12
        return self.fundamental == new_note or self.third == new_note or self.fifth == new_note


class Chord:
    def __init__(self, b: int, t: int, a: int, s: int):
        self.b = b
        self.t = t
        self.a = a
        self.s = s

    @staticmethod
    def of_tuple(notes):
        return Chord(notes[0], notes[1], notes[2], notes[3])

    @staticmethod
    def empty():
        return Chord(-1, -1, -1, -1)

    def simplify(self):
        reduced = [self.b % 12, self.t % 12, self.a % 12, self.s % 12]
        return sorted(list(set(reduced)))

    def fundamental(self):
        return self.b

    def includes(self, note: int):
        return self.b == note or self.t == note or self.a == note or self.s == note

    def to_list(self):
        return [self.b, self.t, self.a, self.s]

    @staticmethod
    def of(chord_list):
        if len(chord_list) == 4:
            return Chord(chord_list[0], chord_list[1], chord_list[2], chord_list[3])
        else:
            return Chord.empty()

    def check_ranges(self):
        abs_range_b: bool = DO <= self.b <= DO + 2 * OCTAVE
        abs_range_t: bool = SOL <= self.t <= SOL + 2 * OCTAVE
        abs_range_a: bool = SOL + 1 * OCTAVE <= self.a <= MI + 3 * OCTAVE
        abs_range_s: bool = DO + 2 * OCTAVE <= self.s <= SOL + 3 * OCTAVE

        absolute_ranges: bool = abs_range_b and abs_range_t and abs_range_a and abs_range_s

        inter_ranges: bool = (self.s - self.a <= 14) and (self.a - self.t <= 14) and (self.t - self.b <= 24)

        return absolute_ranges and inter_ranges

    Do = SimplifiedChord(DO, MI, SOL)
    Re = SimplifiedChord(RE, FA, LA)
    Mi = SimplifiedChord(MI, SOL, SI)
    Fa = SimplifiedChord(FA, LA, DO)
    Sol = SimplifiedChord(SOL, SI, RE)
    La = SimplifiedChord(LA, DO, MI)
    Si = SimplifiedChord(SI, RE, FA)

    mapping = {
        DO: Do,
        RE: Re,
        MI: Mi,
        FA: Fa,
        SOL: Sol,
        LA: La,
        SI: Si
    }

    @staticmethod
    def simple_of(fundamental: int):
        return Chord.mapping[fundamental % 12]

    def __str__(self):
        return "Chord (b:{}, t:{}, a:{}, s:{})".format(self.b, self.t, self.a, self.s)


class ChordTree:
    def __init__(self, root: Chord, depth: int):
        self.root = root
        self.depth = depth


class Node(ChordTree):
    def __init__(self, root: Chord, depth: int, leaves: list):
        super().__init__(root, depth)
        self.leaves = leaves

    def add_leaves(self, leaves: list):
        self.leaves.extend(leaves)


class Leaf(ChordTree):
    def __init__(self, root: Chord, depth: int):
        super().__init__(root, depth)


class Empty(ChordTree):
    def __init(self, depth: int):
        super().__init__(Chord.empty(), depth)


def all_options(tas_options):
    return itertools.product(*tas_options)


def all_in_epsilon(note):
    return range(max(0, note - EPSILON), note + EPSILON + 1)


def complete_transition(current_chord_list, next_chord_list,
                        next_simple_chord):  # check size of epsilon -> handle cases with -1 left
    btas_options = []

    for i, note in zip(range(len(next_chord_list)), next_chord_list):
        if note == -1:
            btas_options.append(list(filter(lambda x: next_simple_chord.includes(x),
                                            list(all_in_epsilon(current_chord_list[i])))))  # add outer list
        else:
            btas_options.append([note])

    return all_options(btas_options)


def filter_w_rules(current_chord_list, options):
    # rule 1 : no duplicate of the seventh note
    temp1 = []
    for chord_i in options:
        ack = 0
        for note in chord_i:
            if note % 12 == SI:
                ack += 1
        if 0 <= ack < 2:
            temp1.append(chord_i)

    # rule 2 : accords are in range
    temp2 = []
    for chord_i in temp1:
        if Chord.of_tuple(chord_i).check_ranges():
            temp2.append(chord_i)

    # rule 3 : seventh (leading) note goes to tonic if grade is V or VII and the following is I, IV or VI
    temp3 = []
    for chord_i in temp2:
        # TODO check if order in tuple (chord_i) is preserved
        prev_fundamental = Chord.simple_of(current_chord_list[0]).fundamental
        fundamental = Chord.simple_of(chord_i[0]).fundamental

        seventh_active = (prev_fundamental == SOL or prev_fundamental == SI) \
                         and (fundamental == DO or fundamental == FA or fundamental == LA)

        for i, note in current_chord_list:
            if not (note % 12 == SI and chord_i[i] % 12 != DO and seventh_active):
                temp3.append(chord_i)

    # rule 4 : a note cannot appear more than 2 times in a chord
    temp4 = []
    for chord_i in temp3:
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))
        correct_dupl = True
        for note in simple_notes_list:
            if simple_notes_list.count(note) > 2:
                correct_dupl = False
        if correct_dupl:
            temp4.append(chord_i)

    # rule 5 : the fifth cannot be repeated
    temp5 = []
    for chord_i in temp4:
        # TODO check if order in tuple (chord_i) is preserved
        fifth = Chord.simple_of(chord_i[0]).fifth
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))
        if not simple_notes_list.count(fifth) > 1:
            temp5.append(chord_i)

    # rule 6 : all notes of the chord are present
    temp6 = []
    for chord_i in temp5:
        simple_chord = Chord.simple_of(chord_i[0])
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))
        if simple_chord.fundamental in simple_notes_list and simple_chord.third in simple_notes_list \
                and simple_chord.fifth in simple_notes_list:
            temp6.append(chord_i)

    # rule 7 : third only duplicated when the fundamental duplication is not recommended or grades are V-VI
    temp7 = []
    for chord_i in temp6:
        fundamental = Chord.simple_of(chord_i[0]).fundamental
        third = Chord.simple_of(chord_i[0]).third
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))

        prev_fundamental = Chord.simple_of(current_chord_list[0]).fundamental

        third_two_times = simple_notes_list.count(third) == 2
        fund_rec = fundamental == DO or fundamental == FA or fundamental == SOL or fundamental == RE
        five_six = prev_fundamental == SOL and fundamental == LA

        if not (third_two_times and fund_rec and not five_six):
            temp7.append(chord_i)

    # rule 8 : forth augmented interval not allowed
    temp8 = []
    for chord_i in temp7:
        for i, note in current_chord_list:
            if not (note % 12 == FA and chord_i[i] % 12 == SI):
                temp8.append(chord_i)

    # rule 9 : two consecutive fourths, fifths and octaves are not allowed
    temp9 = []
    for chord_i in temp8:
        int_problem = False
        for i, note_i in current_chord_list:
            for j, note_j in current_chord_list[i:]:
                if i != j:
                    interval_current = (note_j % 12) - (note_i % 12)
                    interval_next = (chord_i[j] % 12) - (chord_i[i] % 12)
                    if interval_current == interval_next and (
                            interval_current == 0 or interval_current == 5 or interval_current == 7):
                        int_problem = True
        if not int_problem:
            temp9.append(chord_i)

    # rule 10 : direct fourths, fifths and octaves are not allowed
    temp10 = []
    for chord_i in temp9:
        int_problem = False
        for i, note_i in current_chord_list:
            for j, note_j in current_chord_list[i:]:
                interval_next = (chord_i[j] % 12) - (chord_i[i] % 12)
                change_chords_i = chord_i[i] - note_i
                change_chords_j = chord_i[j] - note_j

                if ((change_chords_i > 2 and change_chords_j > 2) or (change_chords_i < -2 and change_chords_j < -2)) \
                        and (interval_next == 0 or interval_next == 5 or interval_next == 7):
                    int_problem = True

        if not int_problem:
            temp9.append(chord_i)

    # TODO rule 11: seventh note in the soprano if it is the final cadence

    return temp10


transition = {}  # dictionary that includes transitions from a chord and a bass note to all the possibilities


def next_chords(current_chord: Chord, next_note: int):
    """
    Returns the all the possible chords that can be harmonised from a bass note and the current chord.
    """
    options = transition.get((current_chord, next_note))

    if options is not None:
        return options
    else:

        options = []
        # Keep common notes
        current_chord_list = current_chord.to_list()
        next_chord_list = [next_note]
        next_simple_chord = Chord.simple_of(next_note)

        if current_chord.fundamental() == next_note:
            options.append(current_chord.to_list())
        else:
            for note in current_chord_list[1:]:
                if next_simple_chord.includes(note):
                    next_chord_list.append(note)
                else:
                    next_chord_list.append(-1)

            options = filter_w_rules(current_chord_list,
                                     complete_transition(current_chord_list, next_chord_list, next_simple_chord))

        return options


def compose():
    """ back in params -> initial_chord: Chord, bass_line: list, empty_composition_tree: ChordTree
    Recursive function that from an initial chord, a bass line and an empty composition tree
    creates a composition tree with all the possible harmonizations.
    """
    start_chord = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
    bass = [DO, FA, SOL, SI, DO, DO, LA, FA, SOL, SOL, DO, FA, SOL, DO, DO]
    actual_chord = start_chord
    succession = []

    for root in bass[1:]:
        succession.append(actual_chord)
        actual_chord = next_chords(actual_chord, root)[0]
        actual_chord = Chord(actual_chord[0], actual_chord[1], actual_chord[2], actual_chord[3])

    compositionTree = Node(start_chord, 1, next_chords(start_chord, bass[1]))

    bass = []
    tenor = []
    alto = []
    soprano = []

    for chord in succession:
        bass.append(chord.b)
        tenor.append(chord.t)
        alto.append(chord.a)
        soprano.append(chord.s)

    return [bass, tenor, alto, soprano]


# conserver les mêmes notes
# aller vers la plus proche
# duplication de la fondamentale / rôle des notes dans la gamme
# sensible vers do et jamais dupliquée
# intervales interdits
# quintes consecutives /!\ 4e 5e octaves

if __name__ == '__main__':
    returned = compose()
    print(returned)
