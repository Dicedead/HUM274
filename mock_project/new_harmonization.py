"""
For the sake of simplicity, we will restrict ourselves to a simple harmonisation, with some assumptions:

The key will be C Major.
Each note of the bass line represents its corresponding grade in the key, hence each chord is in fundamental state,
i.e. there are no inversions.
The chords are only formed with fifths, i.e., we do not use seventh or ninth chords.

For the final project, we could implement a much more complex algorithm and objects in order to achieve a bigger variety
of better harmonizations: we could establish less assumptions and add more rules
"""

from itertools import product
from enum import Enum


DO = 0
DO_S_RE_F = 1
RE = 2
RE_S_MI_F = 3
MI = 4
FA = 5
FA_S_SOL_F = 6
SOL = 7
SOL_S_LA_F = 8
LA = 9
LA_S_SI_F = 10
SI = 11
OCTAVE = 12

TONIC = 0
SUPERTONIC = 1
MEDIANT = 2
SUBDOMINANT = 3
DOMINANT = 4
SUBMEDIANT = 5
LEADING_TONE = 6

PERFECT_FIFTH_INTERVAL = 7
PERFECT_FOURTH_INTERVAL = 5


def new_tonality_sharp(prev_tonality):
    return [(note + PERFECT_FIFTH_INTERVAL) % 12 for note in prev_tonality]


def new_tonality_flat(prev_tonality):
    return [(note + PERFECT_FOURTH_INTERVAL) % 12 for note in prev_tonality]


class Tonality(Enum):
    DO_MAJOR = [DO, RE, MI, FA, SOL, LA, SI]
    # A_MINOR = [LA, SI, DO, RE, MI, FA, SOL_S_LA_F]

    SOL_MAJOR = new_tonality_sharp(DO_MAJOR)
    # MI_MINOR = new_tonality_sharp(A_MINOR)

    RE_MAJOR = new_tonality_sharp(SOL_MAJOR)
    # SI_MINOR = new_tonality_sharp(MI_MINOR)

    LA_MAJOR = new_tonality_sharp(RE_MAJOR)
    # FA_S_MINOR = new_tonality_sharp(SI_MINOR)

    MI_MAJOR = new_tonality_sharp(LA_MAJOR)
    # DO_S_MINOR = new_tonality_sharp(FA_S_MINOR)

    SI_MAJOR = new_tonality_sharp(MI_MAJOR)
    # SOL_S_MINOR = new_tonality_sharp(DO_S_MINOR)

    FA_S_MAJOR = new_tonality_sharp(SI_MAJOR)
    # RE_S_MINOR = new_tonality_sharp(SOL_S_MINOR)

    DO_S_MAJOR = new_tonality_sharp(FA_S_MAJOR)
    # LA_S_MINOR = new_tonality_sharp(RE_S_MINOR)

    FA_MAJOR = [FA, SOL, LA, LA_S_SI_F, DO, RE, MI]
    # RE_MINOR = [RE, MI, FA, SOL, LA, LA_S_SI_F, DO_S_RE_F]

    SI_F_MAJOR = new_tonality_flat(FA_MAJOR)
    # SOL_MINOR = new_tonality_flat(RE_MINOR)

    MI_F_MAJOR = new_tonality_flat(SI_F_MAJOR)
    # DO_MINOR = new_tonality_flat(SOL_MINOR)

    LA_F_MAJOR = new_tonality_flat(MI_F_MAJOR)
    # FA_MINOR = new_tonality_flat(DO_MINOR)

    RE_F_MAJOR = new_tonality_flat(LA_F_MAJOR)
    # SI_F_MINOR = new_tonality_flat(FA_MINOR)

    SOL_F_MAJOR = new_tonality_flat(RE_F_MAJOR)
    # MI_F_MINOR = new_tonality_flat(SI_F_MINOR)

    DO_F_MAJOR = new_tonality_flat(SOL_F_MAJOR)
    # LA_F_MINOR = new_tonality_flat(MI_F_MINOR)

    FA_F_MAJOR = new_tonality_flat(DO_F_MAJOR)
    # RE_F_MINOR = new_tonality_flat(LA_F_MINOR)


noteOf = {DO: "Do",
          DO_S_RE_F: "Do#/Reb",
          RE: "Re",
          RE_S_MI_F: "Re#/Mib",
          MI: "Mi",
          FA: "Fa",
          FA_S_SOL_F: "Fa#/Solb",
          SOL: "Sol",
          SOL_S_LA_F: "Sol#/Lab",
          LA: "La",
          LA_S_SI_F: "La#/Sib",
          SI: "Si"}

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
        if len(notes) == 4:
            return Chord(notes[0], notes[1], notes[2], notes[3])
        else:
            return Chord.empty()

    def __eq__(self, that):
        if isinstance(that, Chord):
            return self.b == that.b and self.t == that.t and self.a == that.a and self.s == that.s
        else:
            return False

    def __hash__(self):
        return hash((self.b, self.t, self.a, self.s))

    @staticmethod
    def empty():
        return Chord(-1, -1, -1, -1)

    def simplify(self):
        reduced = [self.b % 12, self.t % 12, self.a % 12, self.s % 12]
        return sorted(list({i for i in reduced}))

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

    @staticmethod
    def simple_of(fundamental: int, tonality_simple: list):
        new_fundamental = fundamental % 12
        ind_fund = tonality_simple.index(new_fundamental)
        return SimplifiedChord(tonality_simple[ind_fund], tonality_simple[(ind_fund + 2) % 7], tonality_simple[(ind_fund + 4) % 7])

    def __str__(self):
        return "Chord (b:{}, t:{}, a:{}, s:{})".format(self.b, self.t, self.a, self.s)


class ChordTree:
    def __init__(self, root: Chord, depth: int):
        self.root = root
        self.depth = depth

    def __str__(self):
        return "\t" * (self.depth - 1) + str(self.root) + " (" + str(self.depth) + ")" + "\n"


class Leaf(ChordTree):

    def __init__(self, root: Chord, depth: int):
        super().__init__(root, depth)

    def __str__(self):
        notes = noteOf[self.root.b % 12] + ", " + noteOf[self.root.t % 12] + ", " \
                + noteOf[self.root.a % 12] + ", " + noteOf[self.root.s % 12]

        return "\t" * (self.depth - 1) + str(self.root) + " (" + notes + ")" + " (" + str(self.depth) + ")" + "\n"

    def level(self):
        return 1

    def total_depth(self):
        return self.depth


class Node(ChordTree):

    def __init__(self, root: Chord, depth: int, children: list):
        super().__init__(root, depth)
        self.children = children

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)

    def __str__(self):
        notes = noteOf[self.root.b % 12] + ", " + noteOf[self.root.t % 12] + ", " \
                + noteOf[self.root.a % 12] + ", " + noteOf[self.root.s % 12]
        ret = "\t" * (self.depth - 1) + str(self.root) + " (" + notes + ")" + " (" + str(self.depth) + ")" + "\n"

        for child in self.children:
            ret += str(child)
        return ret

    def level(self):
        children_count = 0
        for child in self.children:
            children_count += child.level()
        return children_count

    def total_depth(self):
        max_depth = 1
        for child in self.children:
            child_total_depth = child.total_depth()
            if child_total_depth > max_depth:
                max_depth = child_total_depth
        return max_depth


class Empty(ChordTree):
    def __init(self, depth: int):
        super().__init__(Chord.empty(), depth)

    def __str__(self):
        print("Empty")


def all_options(tas_options):
    return {i for i in product(*tas_options)}


def all_in_epsilon(note):
    return range(max(0, note - EPSILON), note + EPSILON + 1)


def complete_transition(current_chord_list, next_chord_list,
                        next_simple_chord: SimplifiedChord):  # check size of epsilon -> handle cases with -1 left
    btas_options = []

    for i, note in enumerate(next_chord_list):
        if note == -1:
            btas_options.append(list(filter(lambda x: next_simple_chord.includes(x),
                                            list(all_in_epsilon(current_chord_list[i])))))  # add outer list
        else:
            btas_options.append([note])

    return all_options(btas_options)


def filter_w_rules(current_chord_list, options, is_cadence: bool, tonality_rules_input: Tonality):

    # FIXME: check augmented intervals!! (SOL MAJOR: fa# - do descending)

    tonality_rules = tonality_rules_input.value

    # rule 1 : no duplicate of the seventh note
    temp1 = set()
    for chord_i in options:
        ack = 0
        for note in chord_i:
            if note % 12 == tonality_rules[LEADING_TONE]:
                ack += 1
        if 0 <= ack < 2:
            temp1.add(chord_i)

    # rule 2 : accords are in range
    temp2 = set()
    for chord_i in temp1:
        if Chord.of_tuple(chord_i).check_ranges():
            temp2.add(chord_i)

    # rule 3 : seventh (leading) note goes to tonic if grade is V or VII and the following is I, IV or VI
    temp3 = set()
    for chord_i in temp2:
        prev_fundamental = Chord.simple_of(current_chord_list[0], tonality_rules).fundamental
        fundamental = Chord.simple_of(chord_i[0], tonality_rules).fundamental

        seventh_active = (prev_fundamental == tonality_rules[DOMINANT] or prev_fundamental == tonality_rules[LEADING_TONE]) \
                         and (fundamental == tonality_rules[TONIC] or fundamental == tonality_rules[SUBDOMINANT]
                              or fundamental == tonality_rules[SUBMEDIANT])

        for i, note in enumerate(current_chord_list):
            if not (note % 12 == tonality_rules[LEADING_TONE] and chord_i[i] % 12 != tonality_rules[TONIC] and seventh_active):
                temp3.add(chord_i)

    # rule 4 : a note cannot appear more than 2 times in a chord
    temp4 = set()
    for chord_i in temp3:
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))
        correct_dupl = True
        for note in simple_notes_list:
            if simple_notes_list.count(note) > 2:
                correct_dupl = False
        if correct_dupl:
            temp4.add(chord_i)

    # rule 5 : the fifth cannot be repeated
    temp5 = set()
    for chord_i in temp4:
        fifth = Chord.simple_of(chord_i[0], tonality_rules).fifth
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))
        if not simple_notes_list.count(fifth) > 1:
            temp5.add(chord_i)

    # rule 6 : all notes of the chord are present
    temp6 = set()
    for chord_i in temp5:
        simple_chord = Chord.simple_of(chord_i[0], tonality_rules)
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))
        if simple_chord.fundamental in simple_notes_list and simple_chord.third in simple_notes_list \
                and simple_chord.fifth in simple_notes_list:
            temp6.add(chord_i)

    # rule 7 : third only duplicated when the fundamental duplication is not recommended or grades are V-VI
    temp7 = set()
    for chord_i in temp6:
        fundamental = Chord.simple_of(chord_i[0], tonality_rules).fundamental
        third = Chord.simple_of(chord_i[0], tonality_rules).third
        simple_notes_list = list(map(lambda x: x % 12, list(chord_i)))

        prev_fundamental = Chord.simple_of(current_chord_list[0], tonality_rules).fundamental

        third_two_times = simple_notes_list.count(third) == 2
        fund_rec = fundamental == tonality_rules[TONIC] or fundamental == tonality_rules[SUBDOMINANT] \
                   or fundamental == tonality_rules[DOMINANT] or fundamental == tonality_rules[SUPERTONIC]
        five_six = prev_fundamental == tonality_rules[DOMINANT] and fundamental == tonality_rules[SUBMEDIANT]

        if not (third_two_times and fund_rec and not five_six):
            temp7.add(chord_i)

    # rule 8 : fourth augmented interval not allowed
    temp8 = set()
    for chord_i in temp7:
        for i, note in enumerate(current_chord_list):
            if not (note % 12 == tonality_rules[SUBDOMINANT] and chord_i[i] % 12 == tonality_rules[LEADING_TONE]):
                temp8.add(chord_i)

    # rule 9 : two consecutive fourths, fifths and octaves are not allowed
    temp9 = set()
    for chord_it in temp8:
        int_problem = False
        for i, note_i in enumerate(current_chord_list):
            for j in range(i, 4):
                if i != j:
                    mov = current_chord_list[j] != chord_it[j] or note_i != chord_it[i]

                    interval_current = (current_chord_list[j] - note_i) % 12
                    interval_next = (chord_it[j] - chord_it[i]) % 12
                    if interval_current == interval_next and mov and \
                            (interval_current == 0 or interval_current == 5 or interval_current == 7):
                        int_problem = True
        if not int_problem:
            temp9.add(chord_it)

    # rule 10 : direct fourths, fifths and octaves are not allowed
    temp10 = set()
    for chord_i in temp9:
        int_problem = False
        for i, note_i in enumerate(current_chord_list):
            for j in range(i, 4):
                if i != j:
                    interval_next = chord_i[j] - chord_i[i]
                    change_chords_i = chord_i[i] - note_i
                    change_chords_j = chord_i[j] - current_chord_list[j]

                    if ((change_chords_i > 2 and change_chords_j > 2) or (
                            change_chords_i < -2 and change_chords_j < -2)) \
                            and (interval_next == 0 or interval_next == 5 or interval_next == 7):
                        int_problem = True

        if not int_problem:
            temp10.add(chord_i)

    # rule 11 : seventh note and tonic note in the soprano if it is the final cadence
    temp11 = set()
    if (not is_cadence) or current_chord_list[0] % 12 == tonality_rules[LEADING_TONE]:
        return temp10
    else:
        for chord_i in temp10:
            if current_chord_list[3] % 12 == tonality_rules[LEADING_TONE] and chord_i[3] % 12 == tonality_rules[TONIC]:
                temp11.add(chord_i)

    return temp11


transition = {}  # dictionary that includes transitions from a chord and a bass note to all the possibilities


def next_chords(current_chord: Chord, next_note: int, is_cadence: bool, tonality_chords: Tonality):
    global transition
    """
    Returns all the possible chords that can be harmonised from the current chord and a bass note.
    """
    options = transition.get((current_chord, next_note))

    if options is not None:
        return options
    else:

        options = set()

        # Keep common notes
        current_chord_list = current_chord.to_list()
        next_chord_list = [next_note]

        next_simple_chord = Chord.simple_of(next_note, tonality_chords.value)

        if current_chord.fundamental() == next_note:
            options.add(tuple(current_chord.to_list()))
        else:
            for note in current_chord_list[1:]:
                if next_simple_chord.includes(note):
                    if note % 12 != tonality_chords.value[LEADING_TONE]:
                        next_chord_list.append(note)
                    else:
                        next_chord_list.append(-1)
                else:
                    next_chord_list.append(-1)

            options = filter_w_rules(current_chord_list,
                                     complete_transition(current_chord_list, next_chord_list, next_simple_chord),
                                     is_cadence,
                                     tonality_chords)

        transition[(current_chord, next_note)] = tuple(opt for opt in options)
        return transition[(current_chord, next_note)]


def compose(initial_chord, bass_line, prev_chord_tree, tonality_compose):
    """
    Recursive function that from an initial chord, a bass line and an empty composition tree
    creates a composition tree with all the possible harmonizations.
    """
    if len(bass_line) > 1:
        list_next_chords = next_chords(initial_chord, bass_line[0], False, tonality_compose)

        for chord in list_next_chords:
            chord_type = Chord(chord[0], chord[1], chord[2], chord[3])
            node = Node(chord_type, prev_chord_tree.depth + 1, [])
            prev_chord_tree.add_child(node)
            compose(chord_type, bass_line[1:], node, tonality_compose)

    else:
        if len(bass_line) == 1:
            list_next_chords = next_chords(initial_chord, bass_line[0], True, tonality_compose)

            for chord in list_next_chords:
                chord_type = Chord(chord[0], chord[1], chord[2], chord[3])
                leaf = Leaf(chord_type, prev_chord_tree.depth + 1)
                prev_chord_tree.add_child(leaf)


if __name__ == '__main__':

    start_chord_do_major = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
    bass_do_major = [DO, FA, SOL, SI, DO + OCTAVE, FA, LA, FA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]

    start_chord = Chord(SOL, SI + 1 * OCTAVE, SOL + 2 * OCTAVE, RE + 3 * OCTAVE)
    bass = [note + PERFECT_FIFTH_INTERVAL for note in bass_do_major]
    tonality = Tonality.SOL_MAJOR

    compositionTree = Node(start_chord, 1, [])
    compose(start_chord, bass[1:], compositionTree, tonality)

    print(compositionTree)
    print(compositionTree.level())
