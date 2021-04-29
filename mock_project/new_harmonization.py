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

# NOTES IN THE DIATONIC SCALE
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

# Map from a note (integer) to its corresponding string.
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

# SCALE DEGREES 0-BASED
TONIC = 0
SUPERTONIC = 1
MEDIANT = 2
SUBDOMINANT = 3
DOMINANT = 4
SUBMEDIANT = 5
LEADING_TONE = 6

# INTERVALS AND ITS CORRESPONDING AMOUNT OF SEMITONES
UNISON = 0
MINOR_THIRD_INTERVAL = 3
MAJOR_THIRD_INTERVAL = 4
PERFECT_FOURTH_INTERVAL = 5
PERFECT_FIFTH_INTERVAL = 7
OCTAVE = 12

###########################################
#          PARAMETERS WE CAN FIT          #
###########################################

EPSILON = 7  # allowed delta between two notes from different adjacent voices when looking for a transition
MAINTAIN_COMMON_NOTES = False  # prioritizes maintaining the common notes when chaining two chords
OVERTAKING_CADENCE = 0  # max. overtaking allowed between two voices when there is a cadence
OVERTAKING_NO_CADENCE = -4  # max. overtaking allowed between two voices when there is not a cadence

RULE_0_ACTIVE = True  # rule 0 : no big overtaking between voices
RULE_1_ACTIVE = True  # rule 1 : no duplication of the leading note
RULE_2_ACTIVE = True  # rule 2 : chords are in (absolute) range
RULE_3_ACTIVE = True  # rule 3 : leading note goes to tonic if grade is V or VII and the following is I, IV or VI
RULE_4_ACTIVE = True  # rule 4 : a note cannot appear more than 2 times in a chord
RULE_5_ACTIVE = True  # rule 5 : the fifth note has to be repeated for VII degree and cannot be repeated otherwise
RULE_6_ACTIVE = True  # rule 6 : all notes of the chord are present
RULE_7_ACTIVE = True  # rule 7 : third duplication (not I, IV, V) and V -> VI (m - M), VI -> V (m)
RULE_8_ACTIVE = True  # rule 8 : fourth augmented interval not allowed
RULE_9_ACTIVE = True  # rule 9 : two consecutive fourths, fifths and octaves are not allowed
RULE_10_ACTIVE = True  # rule 10 : direct fourths, fifths and octaves are not allowed
RULE_11_ACTIVE = True  # rule 11 : leading note and tonic note in the soprano if it is the final cadence

# NOTE RANGES WHERE BASS, TENOR, ALTO AND SOPRANO CAN BE PLACED
MIN_B = DO
MAX_B = DO + 2 * OCTAVE
MIN_T = SOL
MAX_T = SOL + 2 * OCTAVE
MIN_A = SOL + 1 * OCTAVE
MAX_A = MI + 3 * OCTAVE
MIN_S = DO + 2 * OCTAVE
MAX_S = LA + 3 * OCTAVE


###########################################
#            UTILITIES FOR KEYS           #
###########################################

# Creates a new key with one more sharp from the prev_key.
def new_key_sharp(prev_key):
    return [(note + PERFECT_FIFTH_INTERVAL) % 12 for note in prev_key]


# Creates a new key with one more flat from the prev_key.
def new_key_flat(prev_key):
    return [(note + PERFECT_FOURTH_INTERVAL) % 12 for note in prev_key]


# Returns whether a key is major or not.
def is_major(key_min_maj):
    return abs(key_min_maj[MEDIANT] - key_min_maj[TONIC]) == MAJOR_THIRD_INTERVAL


# Enum type which represents keys as lists. From 7 flats to 7 sharps.
class Key(Enum):
    DO_MAJOR = [DO, RE, MI, FA, SOL, LA, SI]
    LA_MINOR = [LA, SI, DO, RE, MI, FA, SOL_S_LA_F]

    # KEYS WITH SHARP :

    SOL_MAJOR = new_key_sharp(DO_MAJOR)
    MI_MINOR = new_key_sharp(LA_MINOR)

    RE_MAJOR = new_key_sharp(SOL_MAJOR)
    SI_MINOR = new_key_sharp(MI_MINOR)

    LA_MAJOR = new_key_sharp(RE_MAJOR)
    FA_S_MINOR = new_key_sharp(SI_MINOR)

    MI_MAJOR = new_key_sharp(LA_MAJOR)
    DO_S_MINOR = new_key_sharp(FA_S_MINOR)

    SI_MAJOR = new_key_sharp(MI_MAJOR)
    SOL_S_MINOR = new_key_sharp(DO_S_MINOR)

    FA_S_MAJOR = new_key_sharp(SI_MAJOR)
    RE_S_MINOR = new_key_sharp(SOL_S_MINOR)

    DO_S_MAJOR = new_key_sharp(FA_S_MAJOR)
    LA_S_MINOR = new_key_sharp(RE_S_MINOR)

    # KEYS WITH FLAT :

    FA_MAJOR = new_key_flat(DO_MAJOR)
    RE_MINOR = new_key_flat(LA_MINOR)

    SI_F_MAJOR = new_key_flat(FA_MAJOR)
    SOL_MINOR = new_key_flat(RE_MINOR)

    MI_F_MAJOR = new_key_flat(SI_F_MAJOR)
    DO_MINOR = new_key_flat(SOL_MINOR)

    LA_F_MAJOR = new_key_flat(MI_F_MAJOR)
    FA_MINOR = new_key_flat(DO_MINOR)

    RE_F_MAJOR = new_key_flat(LA_F_MAJOR)
    SI_F_MINOR = new_key_flat(FA_MINOR)

    SOL_F_MAJOR = new_key_flat(RE_F_MAJOR)
    MI_F_MINOR = new_key_flat(SI_F_MINOR)

    DO_F_MAJOR = new_key_flat(SOL_F_MAJOR)
    LA_F_MINOR = new_key_flat(MI_F_MINOR)


###########################################
#             DATA STRUCTURES             #
###########################################

# Class that represents a chord of three notes which are in the range 0 to 11 (both included).
class SimplifiedChord:
    def __init__(self, fundamental: int, third: int, fifth: int):
        self.fundamental = fundamental % 12
        self.third = third % 12
        self.fifth = fifth % 12

    # Determines whether the (simplified) given note is included in the chord
    def includes(self, note: int):
        new_note = note % 12
        return self.fundamental == new_note or self.third == new_note or self.fifth == new_note


# Class which represents a chord of four notes. The voices are, in order, the bass, the tenor, the alto and the soprano.
class Chord:
    def __init__(self, b: int, t: int, a: int, s: int):
        self.b = b
        self.t = t
        self.a = a
        self.s = s

    # Returns a Chord from a tuple.
    @staticmethod
    def of_tuple(notes):
        if len(notes) == 4:
            return Chord(notes[0], notes[1], notes[2], notes[3])
        else:
            return Chord.empty()

    # Returns the empty Chord.
    @staticmethod
    def empty():
        return Chord(-1, -1, -1, -1)

    # Creates a new Chord with notes in range 0 - 11 and ordered.
    def simplify(self):
        reduced = [self.b % 12, self.t % 12, self.a % 12, self.s % 12]
        return sorted(list({i for i in reduced}))

    # Returns the fundamental of the Chord.
    def fundamental(self):
        return self.b

    # Determines whether the Chord contains the note or not.
    def includes(self, note: int):
        return self.b == note or self.t == note or self.a == note or self.s == note

    # Transforms a Chord into its equivalent list.
    def to_list(self):
        return [self.b, self.t, self.a, self.s]

    # Creates a Chord from a list.
    @staticmethod
    def of(chord_list):
        if len(chord_list) == 4:
            return Chord(chord_list[0], chord_list[1], chord_list[2], chord_list[3])
        else:
            return Chord.empty()

    # Checks whether the notes respect the voice range constraints or not.
    def check_abs_ranges(self):
        abs_range_b = MIN_B <= self.b <= MAX_B
        abs_range_t = MIN_T <= self.t <= MAX_T
        abs_range_a = MIN_A <= self.a <= MAX_A
        abs_range_s = MIN_S <= self.s <= MAX_S

        return abs_range_b and abs_range_t and abs_range_a and abs_range_s

    # Checks if the number of semitones between adjacent voices is correct.
    def check_inter_ranges(self):
        return (abs(self.s - self.a) <= 14) and (abs(self.a - self.t) <= 14) and (abs(self.t - self.b) <= 24)

    # Check if the ranges of the voices are correct from their absolute and inter ranges.
    def check_ranges(self):
        return self.check_abs_ranges() and self.check_inter_ranges()

    # Creates a new SimplifiedChord from a fundamental note and a key.
    @staticmethod
    def simple_of(fundamental: int, key_simple: list):
        new_fundamental = fundamental % 12
        ind_fund = key_simple.index(new_fundamental)
        return SimplifiedChord(key_simple[ind_fund], key_simple[(ind_fund + 2) % 7],
                               key_simple[(ind_fund + 4) % 7])

    def __eq__(self, that):
        if isinstance(that, Chord):
            return self.b == that.b and self.t == that.t and self.a == that.a and self.s == that.s
        else:
            return False

    def __hash__(self):
        return hash((self.b, self.t, self.a, self.s))

    def __str__(self):
        return "Chord (b:{}, t:{}, a:{}, s:{})".format(self.b, self.t, self.a, self.s)


# Class which represents a tree of Chord.
class ChordTree:
    def __init__(self, root: Chord, depth: int):
        self.root = root
        self.depth = depth

    def __str__(self):
        return "\t" * (self.depth - 1) + str(self.root) + " (" + str(self.depth) + ")" + "\n"


# Class that represents a leaf (a form of ChordTree).
# The leaf is formed of a root and has a depth (within its parent ChordTree).
class Leaf(ChordTree):

    def __init__(self, root: Chord, depth: int):
        super().__init__(root, depth)

    # Returns a 1 level as it is a leaf.
    def level(self):
        return 1

    # Returns its total depth within its parent ChordTree.
    def total_depth(self):
        return self.depth

    def __str__(self):
        notes = noteOf[self.root.b % 12] + ", " + noteOf[self.root.t % 12] + ", " \
                + noteOf[self.root.a % 12] + ", " + noteOf[self.root.s % 12]

        return "\t" * (self.depth - 1) + str(self.root) + " (" + notes + ")" + " (" + str(self.depth) + ")" + "\n"


# Class that represents a node (a form of ChordTree). It has a root, a depth (within its parent ChordTree)
# and a list of children (of type ChordTree).
class Node(ChordTree):

    def __init__(self, root: Chord, depth: int, children: list):
        super().__init__(root, depth)
        self.children = children

    # Adds a child to the node.
    def add_child(self, child):
        self.children.append(child)

    # Adds a list of children to the node.
    def add_children(self, children):
        self.children.extend(children)

    # Returns the total number of leaves the node contains as a ChordTree.
    def level(self):
        children_count = 0
        for child in self.children:
            children_count += child.level()
        return children_count

    # Returns the largest total depth of its children as a ChordTree.
    def total_depth(self):
        max_depth = 1
        for child in self.children:
            child_total_depth = child.total_depth()
            if child_total_depth > max_depth:
                max_depth = child_total_depth
        return max_depth

    def __str__(self):
        notes = noteOf[self.root.b % 12] + ", " + noteOf[self.root.t % 12] + ", " \
                + noteOf[self.root.a % 12] + ", " + noteOf[self.root.s % 12]
        ret = "\t" * (self.depth - 1) + str(self.root) + " (" + notes + ")" + " (" + str(self.depth) + ")" + "\n"

        for child in self.children:
            ret += str(child)
        return ret


# Class that represents a empty node (a form of ChordTree). It has a depth (within its parent ChordTree).
class Empty(ChordTree):
    def __init__(self, depth: int):
        super().__init__(Chord.empty(), depth)

    def __str__(self):
        print("Empty")


###########################################
#          HARMONISATION METHODS          #
###########################################

# Auxiliary method which returns the cartesian product of chords (as lists) for all the simple_options.
def all_options(simple_options):
    return {i for i in product(*simple_options)}


# Auxiliary method that returns a range (of notes) within the epsilon value.
def all_in_epsilon(note):
    return range(max(0, note - EPSILON), note + EPSILON + 1)


# Auxiliary method that completes and returns all the possible transitions between the current chord
# and the next chord, both represented by a list.
# For the notes of the next_chord that are not defined, it creates a list with all the possible values.
# After that, it computes and returns all the different possibilities of chords.
def complete_transition(current_chord_list, next_chord_list, next_simple_chord: SimplifiedChord):
    simple_options = []

    for i, note in enumerate(next_chord_list):

        if note == -1:
            # adds the list for the notes within the range and filters it by the notes included in the next chord
            simple_options.append(list(filter(lambda x: next_simple_chord.includes(x),
                                              list(all_in_epsilon(current_chord_list[i])))))
        else:
            simple_options.append([note])  # the note is already defined

    return all_options(simple_options)  # computes all the options from the simple list (of length 4) of lists


# From current_chord_list (the list that represents the current chord), options (the set of all the possible chords
# chain with the current chord), next_next_degree (the note that represents the degree two positions ahead, -1 if there
# is not), is_cadence (boolean that determines if the next_chord is the final chord of a cadence) and
# key_rules_input (the key).
#
# This method sequentially filters the set of all possible options following the more important harmonic rules.
# The different rules can be deactivated independently thanks to the corresponding constants.
def filter_w_rules(current_chord_list, options, next_next_degree, is_final_cadence, key_rules_input):
    key_degrees = key_rules_input.value

    # The temporary set that changes with respect to the rules
    temp = options.copy()
    ##############################################
    # RULE 0 : NO BIG OVERTAKING BETWEEN VOICES
    temp0 = set()
    for next_chord in temp:

        # intervals between adjacent voices
        b_t_interval = next_chord[1] - next_chord[0]
        t_a_interval = next_chord[2] - next_chord[1]
        a_s_interval = next_chord[3] - next_chord[2]

        # the allowed overtaking between voices depends on whether there is a cadence or not
        not_big_overtake_b_t = b_t_interval >= OVERTAKING_NO_CADENCE if is_final_cadence else b_t_interval >= OVERTAKING_CADENCE
        not_big_overtake_t_a = t_a_interval >= OVERTAKING_NO_CADENCE if is_final_cadence else t_a_interval >= OVERTAKING_CADENCE
        not_big_overtake_a_s = a_s_interval >= OVERTAKING_NO_CADENCE if is_final_cadence else a_s_interval >= OVERTAKING_CADENCE

        if not_big_overtake_b_t and not_big_overtake_t_a and not_big_overtake_a_s:
            temp0.add(next_chord)
    temp = temp0 if RULE_0_ACTIVE else temp

    ##############################################
    # RULE 1 : NO DUPLICATION OF THE LEADING NOTE
    temp1 = set()
    for next_chord in temp:
        ack = 0
        for note in next_chord:
            if note % 12 == key_degrees[LEADING_TONE]:
                ack += 1
        if 0 <= ack < 2:
            temp1.add(next_chord)
    temp = temp1 if RULE_1_ACTIVE else temp

    ##############################################
    # RULE 2 : CHORDS RESPECT CORRECT RANGES
    temp2 = set()
    for next_chord in temp:
        if Chord.of_tuple(next_chord).check_ranges():
            temp2.add(next_chord)
    temp = temp2 if RULE_2_ACTIVE else temp

    ####################################################################
    # RULE 3 : LEADING NOTE GOES TO TONIC IF CURRENT GRADE IS V OR VII
    #          AND THE FOLLOWING IS I, IV OR VI
    temp3 = set()
    for next_chord in temp:

        prev_fund = Chord.simple_of(current_chord_list[0], key_degrees).fundamental
        current_fund = Chord.simple_of(next_chord[0], key_degrees).fundamental

        # determines whether the leading notes is considered active (need to resolve)
        leading_active = (prev_fund == key_degrees[DOMINANT] or prev_fund == key_degrees[LEADING_TONE]) \
                         and (current_fund == key_degrees[TONIC] or current_fund == key_degrees[SUBDOMINANT]
                              or current_fund == key_degrees[SUBMEDIANT])

        for i, curr_note in enumerate(current_chord_list):
            if not leading_active or \
                    (curr_note % 12 == key_degrees[LEADING_TONE] and next_chord[i] % 12 == key_degrees[TONIC]
                     and leading_active):
                temp3.add(next_chord)
    temp = temp3 if RULE_3_ACTIVE else temp

    ##################################################################
    # RULE 4 : A NOTE CANNOT APPEAR MORE THAT 2 TIMES IN A SAME CHORD
    temp4 = set()
    for next_chord in temp:
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))
        correct_dupl = True

        for note in simple_notes_list:
            if simple_notes_list.count(note) > 2:
                correct_dupl = False

        if correct_dupl:
            temp4.add(next_chord)
    temp = temp4 if RULE_4_ACTIVE else temp

    #############################################################################################
    # RULE 5 : THE FIFTH NOTE HAS TO BE REPEATED FOR VII DEGREE AND CANNOT BE REPEATED OTHERWISE
    temp5 = set()
    for next_chord in temp:
        fund = Chord.simple_of(next_chord[0], key_degrees).fundamental
        fifth = Chord.simple_of(next_chord[0], key_degrees).fifth
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))

        if fund % 12 == key_degrees[LEADING_TONE]:
            if simple_notes_list.count(fifth) == 2:
                temp5.add(next_chord)
        elif simple_notes_list.count(fifth) < 2:
            temp5.add(next_chord)
    temp = temp5 if RULE_5_ACTIVE else temp

    ##############################################
    # RULE 6 : ALL NOTES OF THE CHORD ARE PRESENT
    temp6 = set()
    for next_chord in temp:
        simple_next_chord = Chord.simple_of(next_chord[0], key_degrees)
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))

        if simple_next_chord.fundamental in simple_notes_list and simple_next_chord.third in simple_notes_list \
                and simple_next_chord.fifth in simple_notes_list:
            temp6.add(next_chord)
    temp = temp6 if RULE_6_ACTIVE else temp

    ########################################################################################################
    # RULE 7 : THIRD DUPLICATION IS AUTHORISED WHEN THE DEGREE IS NOT I, IV AND V; AND IS MANDATORY WHEN
    #               V -> VI chaining in major and minor tonalities (3rd duplicated in VI)
    #               VI -> V chaining in minor tonality (3rd duplicated in VI)
    #               VII -> I (already implemented because of the 1st and 5st rules, 3rd dup. in VII)
    temp7 = set()
    for next_chord in temp:
        prev_fund = Chord.simple_of(current_chord_list[0], key_degrees).fundamental
        next_fund = Chord.simple_of(next_chord[0], key_degrees).fundamental
        third = Chord.simple_of(next_chord[0], key_degrees).third
        simple_notes_list = list(map(lambda x: x % 12, list(next_chord)))

        third_two_times = simple_notes_list.count(third) == 2

        # third duplication not recommended
        third_not_recom = next_fund == key_degrees[TONIC] or next_fund == key_degrees[SUBDOMINANT] \
                          or next_fund == key_degrees[DOMINANT]

        # V -> VI chaining in major and minor tonalities (3rd dup. in VI)
        v_vi = prev_fund == key_degrees[DOMINANT] and next_fund == key_degrees[SUBMEDIANT]

        # VI -> V chaining in minor tonality (3rd dup. in VI)
        vi_v_minor = next_fund == key_degrees[SUBMEDIANT] and \
                     next_next_degree == key_degrees[DOMINANT] and not is_major(key_degrees)

        mandatory_third = v_vi or vi_v_minor

        if (mandatory_third and third_two_times) or (not mandatory_third and not (third_not_recom and third_two_times)):
            temp7.add(next_chord)
    temp = temp7 if RULE_7_ACTIVE else temp

    #################################################
    # RULE 8 : FOURTH AUGMENTED INTERVAL NOT ALLOWED
    temp8 = set()
    for next_chord in temp:

        has_augm_interval = False
        for i, current_note_i in enumerate(current_chord_list):

            # Current note (and next note) are the leading note
            current_note_leading = current_note_i % 12 == key_degrees[LEADING_TONE]
            next_note_leading = next_chord[i] % 12 == key_degrees[LEADING_TONE]

            # Ascending augmented forth interval
            aug_forth_asc = current_note_i % 12 == key_degrees[SUBDOMINANT] and \
                            next_note_leading and \
                            next_chord[i] - current_note_i == 6

            # Descending augmented forth interval
            aug_forth_des = current_note_leading and \
                            next_chord[i] % 12 == key_degrees[SUBDOMINANT] and \
                            current_note_i - next_chord[i] == 6

            # Ascending augmented second interval
            aug_second_asc = current_note_i % 12 == key_degrees[SUBMEDIANT] and \
                             next_note_leading and \
                             next_chord[i] - current_note_i == 3

            # Descending augmented second interval
            aug_second_des = current_note_leading and \
                             next_chord[i] % 12 == key_degrees[SUBDOMINANT] and \
                             current_note_i - next_chord[i] == 3

            # Ascending augmented fifth interval
            aug_fifth_asc = current_note_i % 12 == key_degrees[MEDIANT] and \
                            next_note_leading and \
                            next_chord[i] - current_note_i == 8

            # Descending augmented fifth interval
            aug_fifth_des = current_note_leading and \
                            next_chord[i] % 12 == key_degrees[MEDIANT] and \
                            current_note_i - next_chord[i] == 8

            # If the key is major, augmented intervals can only be fourths
            if is_major(key_degrees):
                if aug_forth_asc or aug_forth_des:
                    has_augm_interval = True

            # If the key is minor, augmented intervals can be fourths, fifths and seconds
            else:
                if aug_forth_asc or aug_forth_des or aug_second_asc or aug_second_des \
                        or aug_fifth_asc or aug_fifth_des:
                    has_augm_interval = True

        if not has_augm_interval:
            temp8.add(next_chord)
    temp = temp8 if RULE_8_ACTIVE else temp

    #########################################################################
    # RULE 9 : TWO CONSECUTIVE FOURTHS, FIFTHS AND OCTAVES ARE NOT ALLOWED
    temp9 = set()
    for next_chord in temp:
        interval_problem = False

        # Compares for the not allowed consecutive intervals between the two chords
        # for all the possible pairs of voices (voice i and a higher voice j)
        for i, note_current_i in enumerate(current_chord_list):
            for j in range(i, 4):
                if i != j:
                    # There is no common note
                    mov = current_chord_list[j] != next_chord[j] or note_current_i != next_chord[i]

                    interval_current = (current_chord_list[j] - note_current_i) % 12
                    interval_next = (next_chord[j] - next_chord[i]) % 12
                    if interval_current == interval_next and mov and \
                            (interval_current == UNISON or interval_current == PERFECT_FOURTH_INTERVAL or
                             interval_current == PERFECT_FIFTH_INTERVAL):
                        interval_problem = True
        if not interval_problem:
            temp9.add(next_chord)
    temp = temp9 if RULE_9_ACTIVE else temp

    #########################################################################
    # RULE 10 : DIRECT FOURTHS, FIFTHS AND OCTAVES ARE NOT ALLOWED
    temp10 = set()
    for next_chord in temp:
        interval_problem = False

        # Compares for the not allowed direct intervals between the two chords
        # for all the possible pairs of voices (voice i and a higher voice j)
        for i, note_current_i in enumerate(current_chord_list):
            for j in range(i, 4):
                if i != j:

                    # An interval is considered direct if both voices change in the same direction
                    # and both for more of a tone
                    interval_next = (next_chord[j] - next_chord[i]) % 12
                    change_chords_i = next_chord[i] - note_current_i
                    change_chords_j = next_chord[j] - current_chord_list[j]

                    if ((change_chords_i > 2 and change_chords_j > 2) or (
                            change_chords_i < -2 and change_chords_j < -2)) \
                            and (interval_next == UNISON or interval_next == PERFECT_FOURTH_INTERVAL
                                 or interval_next == PERFECT_FIFTH_INTERVAL):
                        interval_problem = True

        if not interval_problem:
            temp10.add(next_chord)
    temp = temp10 if RULE_10_ACTIVE else temp

    ###################################################################################
    # RULE 11 : LEADING NOTE AND TONIC NOTE IN THE SOPRANO IF IT IS THE FINAL CADENCE
    temp11 = set()
    if (not is_final_cadence) or current_chord_list[0] % 12 == key_degrees[LEADING_TONE]:
        temp11 = temp10
    else:
        for next_chord in temp:
            if current_chord_list[3] % 12 == key_degrees[LEADING_TONE] and next_chord[3] % 12 == key_degrees[TONIC]:
                temp11.add(next_chord)
    temp = temp11 if RULE_11_ACTIVE else temp

    return temp


# Dictionary that includes transitions from a chord and a the next bass note to all the possible next chords
transition = {}


# Method that from a current_chord, the next_note of the bass, the next_next_note of the bass,
# a boolean is_final_cadence and a key computes all the possible next chords.
def next_chords(current_chord: Chord, next_note: int, next_next_note: int, is_final_cadence: bool, key_for_chords: Key):
    global transition
    """
    Returns all the possible chords that can be harmonised from the current chord and a bass note.
    """
    options = transition.get((current_chord, next_note))

    # If the transition is already computed, it uses it and does not again the computation (dynamic programming)
    if options is not None and not is_final_cadence:
        return options

    else:
        options = set()

        # Keep common notes
        current_chord_list = current_chord.to_list()
        # Already copies the bass note
        next_chord_list = [next_note]
        next_simple_chord = Chord.simple_of(next_note, key_for_chords.value)

        # If the constant MAINTAIN_COMMON_NOTES is true, we keep the common notes in the following chord if possible
        # For the undetermined notes, it adds -1
        if MAINTAIN_COMMON_NOTES:
            if current_chord.fundamental() == next_note:
                options.add(tuple(current_chord.to_list()))
            else:
                for note in current_chord_list[1:]:
                    if next_simple_chord.includes(note) and note % 12 != key_for_chords.value[LEADING_TONE]:
                        next_chord_list.append(note)
                    else:
                        next_chord_list.append(-1)
        else:
            next_chord_list = [next_note, -1, -1, -1]

        # Computes of the possible options for the next chord thanks to the filter_w_rules method
        options = filter_w_rules(current_chord_list,
                                 complete_transition(current_chord_list, next_chord_list, next_simple_chord),
                                 next_next_note,
                                 is_final_cadence,
                                 key_for_chords)

        # Adds the current transition to the global dictionary
        transition[(current_chord, next_note)] = tuple(opt for opt in options)
        return transition[(current_chord, next_note)]


# Recursive method that from an initial_chord, a bass_line, a ChordTree (prev_chord_tree) and a tonality (tonality_compose)
# computes algorithmically the composition (computes all the possible harmonizations) and inserts it into the tree.
# A node (or a leaf) of the chord tree keeps track of its previous chord.
def compose(initial_chord, bass_line, prev_chord_tree, tonality_compose):

    if len(bass_line) > 1:
        # All the possible next chords from the current chord
        list_next_chords = next_chords(initial_chord, bass_line[0], bass_line[1], False, tonality_compose)

        for chord in list_next_chords:
            chord_type = Chord(chord[0], chord[1], chord[2], chord[3])
            node = Node(chord_type, prev_chord_tree.depth + 1, [])
            # Adds the next chord to a node and continues the composition
            prev_chord_tree.add_child(node)
            compose(chord_type, bass_line[1:], node, tonality_compose)

    else:
        if len(bass_line) == 1:
            # Notifies next_chords that this is the final cadence
            list_next_chords = next_chords(initial_chord, bass_line[0], -1, True, tonality_compose)

            for chord in list_next_chords:
                chord_type = Chord(chord[0], chord[1], chord[2], chord[3])
                # As it is the final chord, creates a leaf instead of a node
                leaf = Leaf(chord_type, prev_chord_tree.depth + 1)
                prev_chord_tree.add_child(leaf)
