"""
For the sake of simplicity, we will restrict ourselves to a simple harmonisation, with some assumptions:

Each note of the bass line represents its corresponding grade in the key, hence each chord is in fundamental state,
i.e. there are no inversions.
The chords are only formed with fifths, i.e., we do not use seventh or ninth chords.
"""

from itertools import product
from enum import Enum

###########################################
#               CONSTANTS                 #
###########################################

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

UNISON = 0
MINOR_THIRD_INTERVAL = 3
MAJOR_THIRD_INTERVAL = 4
PERFECT_FOURTH_INTERVAL = 5
PERFECT_FIFTH_INTERVAL = 7


###########################################
#          PARAMETERS WE CAN FIT          #
###########################################

EPSILON = 7  # allowed delta between two notes when looking for a transition
MAINTAIN_COMMON_NOTES = False
OVERTAKING_CADENCE = 0
OVERTAKING_NO_CADENCE = -4

RULE_0_ACTIVE = True  # rule 0 : no big overtaking between voices
RULE_1_ACTIVE = True  # rule 1 : no duplication of the leading note
RULE_2_ACTIVE = True  # rule 2 : chords are in (absolute) range
RULE_3_ACTIVE = True  # rule 3 : leading note goes to tonic if grade is V or VII and the following is I, IV or VI
RULE_4_ACTIVE = True  # rule 4 : a note cannot appear more than 2 times in a chord
RULE_5_ACTIVE = True  # rule 5 : the fifth note cannot be repeated
RULE_6_ACTIVE = True  # rule 6 : all notes of the chord are present
RULE_7_ACTIVE = True  # rule 7 : third duplication (not I, IV, V) and V -> VI (m - M), VI -> V (m)
RULE_8_ACTIVE = True  # rule 8 : fourth augmented interval not allowed
RULE_9_ACTIVE = True  # rule 9 : two consecutive fourths, fifths and octaves are not allowed
RULE_10_ACTIVE = True  # rule 10 : direct fourths, fifths and octaves are not allowed
RULE_11_ACTIVE = True  # rule 11 : leading note and tonic note in the soprano if it is the final cadence

MIN_B = DO
MAX_B = DO + 2 * OCTAVE
MIN_T = SOL
MAX_T = SOL + 2 * OCTAVE
MIN_A = SOL + 1 * OCTAVE
MAX_A = MI + 3 * OCTAVE
MIN_S = DO + 2 * OCTAVE
MAX_S = LA + 3 * OCTAVE


def new_tonality_sharp(prev_tonality):
    return [(note + PERFECT_FIFTH_INTERVAL) % 12 for note in prev_tonality]


def new_tonality_flat(prev_tonality):
    return [(note + PERFECT_FOURTH_INTERVAL) % 12 for note in prev_tonality]


def is_major(tonality):
    return abs(tonality[MEDIANT] - tonality[TONIC]) == MAJOR_THIRD_INTERVAL


class Tonality(Enum):
    DO_MAJOR = [DO, RE, MI, FA, SOL, LA, SI]
    LA_MINOR = [LA, SI, DO, RE, MI, FA, SOL_S_LA_F]

    # TONALITIES WITH SHARP :

    SOL_MAJOR = new_tonality_sharp(DO_MAJOR)
    MI_MINOR = new_tonality_sharp(LA_MINOR)

    RE_MAJOR = new_tonality_sharp(SOL_MAJOR)
    SI_MINOR = new_tonality_sharp(MI_MINOR)

    LA_MAJOR = new_tonality_sharp(RE_MAJOR)
    FA_S_MINOR = new_tonality_sharp(SI_MINOR)

    MI_MAJOR = new_tonality_sharp(LA_MAJOR)
    DO_S_MINOR = new_tonality_sharp(FA_S_MINOR)

    SI_MAJOR = new_tonality_sharp(MI_MAJOR)
    SOL_S_MINOR = new_tonality_sharp(DO_S_MINOR)

    FA_S_MAJOR = new_tonality_sharp(SI_MAJOR)
    RE_S_MINOR = new_tonality_sharp(SOL_S_MINOR)

    DO_S_MAJOR = new_tonality_sharp(FA_S_MAJOR)
    LA_S_MINOR = new_tonality_sharp(RE_S_MINOR)

    # TONALITIES WITH FLAT :

    FA_MAJOR = [FA, SOL, LA, LA_S_SI_F, DO, RE, MI]
    RE_MINOR = [RE, MI, FA, SOL, LA, LA_S_SI_F, DO_S_RE_F]

    SI_F_MAJOR = new_tonality_flat(FA_MAJOR)
    SOL_MINOR = new_tonality_flat(RE_MINOR)

    MI_F_MAJOR = new_tonality_flat(SI_F_MAJOR)
    DO_MINOR = new_tonality_flat(SOL_MINOR)

    LA_F_MAJOR = new_tonality_flat(MI_F_MAJOR)
    FA_MINOR = new_tonality_flat(DO_MINOR)

    RE_F_MAJOR = new_tonality_flat(LA_F_MAJOR)
    SI_F_MINOR = new_tonality_flat(FA_MINOR)

    SOL_F_MAJOR = new_tonality_flat(RE_F_MAJOR)
    MI_F_MINOR = new_tonality_flat(SI_F_MINOR)

    DO_F_MAJOR = new_tonality_flat(SOL_F_MAJOR)
    LA_F_MINOR = new_tonality_flat(MI_F_MINOR)

    FA_F_MAJOR = new_tonality_flat(DO_F_MAJOR)
    RE_F_MINOR = new_tonality_flat(LA_F_MINOR)


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

    def check_abs_ranges(self):
        abs_range_b = MIN_B <= self.b <= MAX_B
        abs_range_t = MIN_T <= self.t <= MAX_T
        abs_range_a = MIN_A <= self.a <= MAX_A
        abs_range_s = MIN_S <= self.s <= MAX_S

        return abs_range_b and abs_range_t and abs_range_a and abs_range_s

    def check_inter_ranges(self):
        return (abs(self.s - self.a) <= 14) and (abs(self.a - self.t) <= 14) and (abs(self.t - self.b) <= 24)

    def check_ranges(self):
        return self.check_abs_ranges() and self.check_inter_ranges()

    @staticmethod
    def simple_of(fundamental: int, tonality_simple: list):
        new_fundamental = fundamental % 12
        ind_fund = tonality_simple.index(new_fundamental)
        return SimplifiedChord(tonality_simple[ind_fund], tonality_simple[(ind_fund + 2) % 7],
                               tonality_simple[(ind_fund + 4) % 7])

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


def filter_w_rules(current_chord_list, options, next_next_degree, is_cadence: bool, tonality_rules_input: Tonality):
    tonality_rules = tonality_rules_input.value

    temp_prev = options.copy()

    # rule 0 : no big overtaking between voices
    temp0 = set()
    for next_chord in options:
        b_t_interval = next_chord[1] - next_chord[0]
        t_a_interval = next_chord[2] - next_chord[1]
        a_s_interval = next_chord[3] - next_chord[2]

        not_big_overtake_b_t = b_t_interval >= OVERTAKING_NO_CADENCE if is_cadence else b_t_interval >= OVERTAKING_CADENCE
        not_big_overtake_t_a = t_a_interval >= OVERTAKING_NO_CADENCE if is_cadence else t_a_interval >= OVERTAKING_CADENCE
        not_big_overtake_a_s = a_s_interval >= OVERTAKING_NO_CADENCE if is_cadence else a_s_interval >= OVERTAKING_CADENCE

        if not_big_overtake_b_t and not_big_overtake_t_a and not_big_overtake_a_s:
            temp0.add(next_chord)
    temp_prev = temp0 if RULE_0_ACTIVE else temp_prev

    # rule 1 : no duplication of the leading note
    temp1 = set()
    for next_chord in temp_prev:
        ack = 0
        for note in next_chord:
            if note % 12 == tonality_rules[LEADING_TONE]:
                ack += 1
        if 0 <= ack < 2:
            temp1.add(next_chord)
    temp_prev = temp1 if RULE_1_ACTIVE else temp_prev

    # rule 2 : chords are in (absolute) range
    temp2 = set()
    for next_chord in temp_prev:
        if Chord.of_tuple(next_chord).check_ranges():
            temp2.add(next_chord)
    temp_prev = temp2 if RULE_2_ACTIVE else temp_prev

    # rule 3 : leading note goes to tonic if grade is V or VII and the following is I, IV or VI
    temp3 = set()
    for next_chord in temp_prev:
        prev_fundamental = Chord.simple_of(current_chord_list[0], tonality_rules).fundamental
        fundamental = Chord.simple_of(next_chord[0], tonality_rules).fundamental

        leading_active = (prev_fundamental == tonality_rules[DOMINANT] or prev_fundamental == tonality_rules[
            LEADING_TONE]) \
                         and (fundamental == tonality_rules[TONIC] or fundamental == tonality_rules[SUBDOMINANT]
                              or fundamental == tonality_rules[SUBMEDIANT])

        for i, note in enumerate(current_chord_list):
            if not leading_active or \
                    (note % 12 == tonality_rules[LEADING_TONE] and next_chord[i] % 12 == tonality_rules[
                        TONIC] and leading_active):
                temp3.add(next_chord)
    temp_prev = temp3 if RULE_3_ACTIVE else temp_prev

    # rule 4 : a note cannot appear more than 2 times in a chord
    temp4 = set()
    for next_chord in temp_prev:
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))
        correct_dupl = True
        for note in simple_notes_list:
            if simple_notes_list.count(note) > 2:
                correct_dupl = False
        if correct_dupl:
            temp4.add(next_chord)
    temp_prev = temp4 if RULE_4_ACTIVE else temp_prev

    # rule 5 : the fifth note cannot be repeated
    temp5 = set()
    for next_chord in temp_prev:
        fifth = Chord.simple_of(next_chord[0], tonality_rules).fifth
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))
        if not simple_notes_list.count(fifth) > 1:
            temp5.add(next_chord)
    temp_prev = temp5 if RULE_5_ACTIVE else temp_prev

    # rule 6 : all notes of the chord are present
    temp6 = set()
    for next_chord in temp_prev:
        simple_chord = Chord.simple_of(next_chord[0], tonality_rules)
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))
        if simple_chord.fundamental in simple_notes_list and simple_chord.third in simple_notes_list \
                and simple_chord.fifth in simple_notes_list:
            temp6.add(next_chord)
    temp_prev = temp6 if RULE_6_ACTIVE else temp_prev

    # rule 7 : third duplication is authorised when the degree is not I, IV and V; and is mandatory when
    #   V -> VI chaining in major and minor tonalities (3rd dup. in VI)
    #   VI -> V chaining in minor tonality (3rd dup. in VI)
    #   VII -> I (already implemented because of the 1st and 5st rules, 3rd dup. in VII)
    temp7 = set()
    for next_chord in temp_prev:
        prev_fundamental = Chord.simple_of(current_chord_list[0], tonality_rules).fundamental

        fundamental = Chord.simple_of(next_chord[0], tonality_rules).fundamental
        third = Chord.simple_of(next_chord[0], tonality_rules).third
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))

        third_two_times = simple_notes_list.count(third) == 2

        # third duplication not recommended
        third_not_recom = fundamental == tonality_rules[TONIC] or fundamental == tonality_rules[SUBDOMINANT] \
                          or fundamental == tonality_rules[DOMINANT]

        # V -> VI chaining in major and minor tonalities (3rd dup. in VI)
        V_VI = prev_fundamental == tonality_rules[DOMINANT] and fundamental == tonality_rules[SUBMEDIANT]

        # VI -> V chaining in minor tonality (3rd dup. in VI)
        VI_V_minor = fundamental == tonality_rules[SUBMEDIANT] and \
                     next_next_degree == tonality_rules[DOMINANT] and not is_major(tonality_rules)

        mandatory_third = V_VI or VI_V_minor

        if (mandatory_third and third_two_times) or (not mandatory_third and not (third_not_recom and third_two_times)):
            temp7.add(next_chord)
    temp_prev = temp7 if RULE_7_ACTIVE else temp_prev

    # rule 8 : fourth augmented interval not allowed
    temp8 = set()
    for next_chord in temp_prev:

        has_augm_interval = False
        for i, current_note_i in enumerate(current_chord_list):

            current_note_leading = current_note_i % 12 == tonality_rules[LEADING_TONE]
            next_note_leading = next_chord[i] % 12 == tonality_rules[LEADING_TONE]

            aug_forth_asc = current_note_i % 12 == tonality_rules[SUBDOMINANT] and \
                            next_note_leading and \
                            next_chord[i] - current_note_i == 6

            aug_forth_des = current_note_leading and \
                            next_chord[i] % 12 == tonality_rules[SUBDOMINANT] and \
                            current_note_i - next_chord[i] == 6

            aug_second_asc = current_note_i % 12 == tonality_rules[SUBMEDIANT] and \
                             next_note_leading and \
                             next_chord[i] - current_note_i == 3

            aug_second_des = current_note_leading and \
                             next_chord[i] % 12 == tonality_rules[SUBDOMINANT] and \
                             current_note_i - next_chord[i] == 3

            aug_fifth_asc = current_note_i % 12 == tonality_rules[MEDIANT] and \
                            next_note_leading and \
                            next_chord[i] - current_note_i == 8

            aug_fifth_des = current_note_leading and \
                            next_chord[i] % 12 == tonality_rules[MEDIANT] and \
                            current_note_i - next_chord[i] == 8

            if is_major(tonality_rules):
                if aug_forth_asc or aug_forth_des:
                    has_augm_interval = True
            else:
                if aug_forth_asc or aug_forth_des or aug_second_asc or aug_second_des \
                        or aug_fifth_asc or aug_fifth_des:
                    has_augm_interval = True

        if not has_augm_interval:
            temp8.add(next_chord)

    temp_prev = temp8 if RULE_8_ACTIVE else temp_prev

    # rule 9 : two consecutive fourths, fifths and octaves are not allowed
    temp9 = set()
    for next_chord in temp_prev:
        int_problem = False
        for i, note_current_i in enumerate(current_chord_list):
            for j in range(i, 4):
                if i != j:
                    mov = current_chord_list[j] != next_chord[j] or note_current_i != next_chord[i]

                    interval_current = (current_chord_list[j] - note_current_i) % 12
                    interval_next = (next_chord[j] - next_chord[i]) % 12
                    if interval_current == interval_next and mov and \
                            (interval_current == UNISON or interval_current == PERFECT_FOURTH_INTERVAL or
                             interval_current == PERFECT_FIFTH_INTERVAL):
                        int_problem = True
        if not int_problem:
            temp9.add(next_chord)
    temp_prev = temp9 if RULE_9_ACTIVE else temp_prev

    # rule 10 : direct fourths, fifths and octaves are not allowed
    temp10 = set()
    for next_chord in temp_prev:
        int_problem = False
        for i, note_current_i in enumerate(current_chord_list):
            for j in range(i, 4):
                if i != j:
                    interval_next = next_chord[j] - next_chord[i]
                    change_chords_i = next_chord[i] - note_current_i
                    change_chords_j = next_chord[j] - current_chord_list[j]

                    if ((change_chords_i > 2 and change_chords_j > 2) or (
                            change_chords_i < -2 and change_chords_j < -2)) \
                            and (interval_next == 0 or interval_next == 5 or interval_next == 7):
                        int_problem = True

        if not int_problem:
            temp10.add(next_chord)
    temp_prev = temp10 if RULE_10_ACTIVE else temp_prev

    # rule 11 : leading note and tonic note in the soprano if it is the final cadence
    temp11 = set()
    if (not is_cadence) or current_chord_list[0] % 12 == tonality_rules[LEADING_TONE]:
        temp11 = temp10
    else:
        for next_chord in temp_prev:
            if current_chord_list[3] % 12 == tonality_rules[LEADING_TONE] and next_chord[3] % 12 == tonality_rules[
                TONIC]:
                temp11.add(next_chord)
    temp_prev = temp11 if RULE_11_ACTIVE else temp_prev

    return temp_prev


transition = {}  # dictionary that includes transitions from a chord and a bass note to all the possibilities


def next_chords(current_chord: Chord, next_note: int, next_next_note: int, is_cadence: bool, tonality_chords: Tonality):
    global transition
    """
    Returns all the possible chords that can be harmonised from the current chord and a bass note.
    """
    options = transition.get((current_chord, next_note))

    # FIXME: is_cadence has to be the final cadence, if not, transition will "always" contain the leading note + tonic in the soprano
    if options is not None and not is_cadence:
        return options

    else:
        options = set()

        # Keep common notes
        current_chord_list = current_chord.to_list()
        next_chord_list = [next_note]

        next_simple_chord = Chord.simple_of(next_note, tonality_chords.value)

        if MAINTAIN_COMMON_NOTES:
            if current_chord.fundamental() == next_note:
                options.add(tuple(current_chord.to_list()))
            else:
                for note in current_chord_list[1:]:
                    if next_simple_chord.includes(note) and note % 12 != tonality_chords.value[LEADING_TONE]:
                        next_chord_list.append(note)
                    else:
                        next_chord_list.append(-1)
        else:
            next_chord_list = [next_note, -1, -1, -1]

        options = filter_w_rules(current_chord_list,
                                 complete_transition(current_chord_list, next_chord_list, next_simple_chord),
                                 next_next_note,
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
        list_next_chords = next_chords(initial_chord, bass_line[0], bass_line[1], False, tonality_compose)

        for chord in list_next_chords:
            chord_type = Chord(chord[0], chord[1], chord[2], chord[3])
            node = Node(chord_type, prev_chord_tree.depth + 1, [])
            prev_chord_tree.add_child(node)
            compose(chord_type, bass_line[1:], node, tonality_compose)

    else:
        if len(bass_line) == 1:
            list_next_chords = next_chords(initial_chord, bass_line[0], -1, True, tonality_compose)

            for chord in list_next_chords:
                chord_type = Chord(chord[0], chord[1], chord[2], chord[3])
                leaf = Leaf(chord_type, prev_chord_tree.depth + 1)
                prev_chord_tree.add_child(leaf)


if __name__ == '__main__':
    # start_chord_do_major = Chord(DO, DO + 2 * OCTAVE, SOL + 2 * OCTAVE, MI + 3 * OCTAVE)
    bass_do_major = [DO, FA, SOL, SI, DO + OCTAVE, FA, LA, FA, SOL, SI, DO + OCTAVE, FA, SOL, DO, SOL, DO]
    # bass_do_major2 = [FA, LA, SI, DO, RE + OCTAVE, MI + OCTAVE, LA, SOL, SI, MI]

    start_chord_sol_major = Chord(SOL, SI + 1 * OCTAVE, SOL + 2 * OCTAVE, RE + 3 * OCTAVE)
    bass_sol_major = [note + PERFECT_FIFTH_INTERVAL for note in bass_do_major]

    start_chord_la_minor = Chord(LA, DO + 2 * OCTAVE, LA + 2 * OCTAVE, MI + 3 * OCTAVE)
    bass_la_minor = [LA, RE, MI, SOL_S_LA_F, LA, RE, FA, RE, MI, SOL_S_LA_F, LA, RE, MI, LA, MI, LA]
    bass_la_minor_debug_rule_7 = [LA, FA, MI, LA, MI, FA]

    tonality = Tonality.LA_MINOR
    start_chord = start_chord_la_minor
    bass = bass_la_minor

    print(start_chord_la_minor.check_abs_ranges())
    print(start_chord_la_minor.check_inter_ranges())

    compositionTree = Node(start_chord, 1, [])
    compose(start_chord, bass[1:], compositionTree, tonality)

    print(compositionTree)
    print(compositionTree.level())
