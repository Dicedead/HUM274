from l_system.l_system_implementation import Rule, LSystem
from util import *


def rules_complex():
    rule_a = Rule("A", "BB[+-D+A")
    rule_b = Rule("B", "D[-C""D[-C")
    rule_c = Rule("C", "CD+C-C-")
    rule_d = Rule("D", "A+[D-DD+D")
    return LSystem(rule_a, rule_b, rule_c, rule_d)


def initial_complex():
    return "A+B"


def run_complex_for(n, show_mode=False):
    return rules_complex().run(initial_complex(), n, show_mode)


def sequence_from_string_complex(string: str):
    """
    To use with chars: A, B, C, D, +, -, [
    A: half note
    B: quarter
    C: eighth
    D: sixteenth
    +: add previous and next duration
    -: make previous note a rest (value: -1 * duration of rest)
    [: extend previous duration by 50%
    :param string: input string
    :return: sequence of durations (floats)
    """

    def char_to_duration(c: str, tb: list):
        if c == 'A':
            tb.append(2)
        elif c == 'B':
            tb.append(1)
        elif c == 'C':
            tb.append(1 / 2)
        elif c == 'D':
            tb.append(3 / 4)
        elif c == '[':
            if len(tb) > 0:
                tb[-1] = tb[-1] + 0.5 * tb[-1]
        elif c == '-':
            if len(tb) > 0:
                tb[-1] = -tb[-1]
        return tb[-1]

    def is_duration_char(c: str):
        return c in ['A', 'B', 'C', 'D']

    str_arr = [c for c in string]
    tab = []
    while not len(str_arr) == 0:
        nb_chars_read = 1

        if str_arr[0] == '+' and len(str_arr) >= 2:
            nb_chars_read = 2
            if len(tab) > 0 and is_duration_char(str_arr[1]):
                old_read = tab[-1]
                new_read = char_to_duration(str_arr[1], tab)
                new_dur = fabs(old_read) + fabs(new_read)
                if old_read < 0:
                    new_dur = -new_dur
                tab[-2] = new_dur
                tab = tab[:-1]

        else:
            char_to_duration(str_arr[0], tab)

        str_arr = str_arr[nb_chars_read:]  # remove chars read
    return tab


def rules_bolero():
    """
    Converge to the Bolero snare drum part: A B A C
    where A = the common first half of the two measures
              (one eighth note + 3 sixteenths)
          B = A + 2 eighth notes, the second half of the
              first measure
          C = A + 6 sixteenth notes, the second half of the
              second measure
    """
    return LSystem(
        Rule("A", "ESSS"),
        Rule("B", "ESSSEE"),
        Rule("C", "ESSSSSSSSSZ"),
        Rule("E", "E"),
        Rule("S", "S"),
        Rule("T", "S"),
        Rule("W", "STSTSTTSSE"),
        Rule("X", "WYTTAYYESSYZ"),
        Rule("Y", "BATTWBWTTTTSTTA"),
        Rule("Z", "ABAC")
    )


def initial_bolero():
    return "YWWX"


def run_bolero_for(n, show_mode=False):
    return rules_bolero().run(initial_bolero(), n, show_mode)


def sequence_from_string_bolero(string: str):
    """
    To use with chars in chars_bolero
    Notes with rhythmical values:

    E: eight note
    S: sixteenth note
    T: 32nd note

    A: triplet
    B: two triplets
    C: dotted eight note

    W: quarter note rest
    X: quintuplet
    Y: two quintuplets
    Z: eight note rest

    :param string: input string
    :return: sequence of durations (floats)
    """
    note_durations = {
        "E": 1 / 2,
        "S": 1 / 4,
        "T": 1 / 8,

        "A": 1 / 3,
        "B": 2 / 3,
        "C": 3 / 4,

        "W": -1 / 4,
        "X": 1 / 5,
        "Y": 2 / 5,
        "Z": -1 / 2
    }

    return [note_durations.get(c) for c in string]


def rules_slow():
    rule_a = Rule("A", "BB[+-D+A")
    rule_b = Rule("B", "D[-""D[-")
    rule_d = Rule("D", "A+[D-DD+D")
    return LSystem(rule_a, rule_b, rule_d)


def initial_slow():
    return "A+B"


def run_slow_for(n, show_mode=False):
    return rules_complex().run(initial_complex(), n, show_mode)


def sequence_from_string_slow(string: str):
    """
    To use with chars: A, B, D, -, [
    A: half note
    B: quarter
    D: dotted eighth
    +: add previous and next duration
    -: make previous note a rest (value: -1 * duration of rest)
    [: extend previous duration by 50%
    :param string: input string
    :return: sequence of durations (floats)
    """

    def char_to_duration(c: str, tb: list):
        if c == 'A':
            tb.append(2)
        elif c == 'B':
            tb.append(1)
        elif c == 'D':
            tb.append(3 / 4)
        elif c == '[':
            if len(tb) > 0:
                tb[-1] = tb[-1] + 0.5 * tb[-1]
        elif c == '-':
            if len(tb) > 0:
                tb[-1] = -tb[-1]
        return tb[-1]

    str_arr = [c for c in string]
    tab = []
    while not len(str_arr) == 0:
        char_to_duration(str_arr[0], tab)
        str_arr = str_arr[1:]  # remove chars read
    return tab


def rules_slow_2():
    rule_a = Rule("A", "[BB[+-A+A")
    rule_b = Rule("B", "BB[-""AB[-")
    return LSystem(rule_a, rule_b)


def initial_slow_2():
    return "A+B"


def run_slow_2_for(n, show_mode=False):
    return rules_complex().run(initial_complex(), n, show_mode)


def sequence_from_string_slow_2(string: str):
    """
    To use with chars: A, B, -, [
    A: half note
    B: quarter
    +: add previous and next duration
    -: make previous note a rest (value: -1 * duration of rest)
    [: extend previous duration by 50%
    :param string: input string
    :return: sequence of durations (floats)
    """

    def char_to_duration(c: str, tb: list):
        if c == 'A':
            tb.append(2)
        elif c == 'B':
            tb.append(1.5)
        elif c == '[':
            if len(tb) > 0:
                tb[-1] = tb[-1] + 0.5 * tb[-1]
        elif c == '-':
            if len(tb) > 0:
                tb[-1] = -tb[-1]
        return tb[-1]

    str_arr = [c for c in string]
    tab = []
    while not len(str_arr) == 0:
        char_to_duration(str_arr[0], tab)
        str_arr = str_arr[1:]  # remove chars read

    return tab


def rules_complex_orig():
    rule_a = Rule("A", "BB[+E-D+A]")
    rule_b = Rule("B", "D[E]-C""D[E]-C")
    rule_c = Rule("C", "CD+C-C-")
    rule_d = Rule("D", "AE+[D-D]D+ED")
    rule_e = Rule("E", "[E+-]B")
    return LSystem(rule_a, rule_b, rule_c, rule_d, rule_e)


def initial_complex_orig():
    return "F]AEE-B"


def chars_complex_orig():
    return ["A", "B", "C", "D", "E"]


def run_complex_orig_for(n, show_mode=False):
    return rules_complex_orig().run(initial_complex_orig(), n, show_mode)


def sequence_from_string_complex_orig(string: str):
    """
    To use with chars: A, B, C, D, E, +, -, [, ]
    A: half note
    B: quarter
    C: eighth
    D: sixteenth
    E: triplet
    +: add previous and next duration
    -: make previous note a rest (value: -1 * duration of rest)
    [: extend previous duration by 50%
    ]: divide previous duration by 2
    :param string: input string
    :return: sequence of durations
    """

    def char_to_duration(c: str, tb: list):
        if c == 'A':
            tb.append(2)
        elif c == 'B':
            tb.append(1)
        elif c == 'C':
            tb.append(1 / 2)
        elif c == 'D':
            tb.append(1 / 4)
        elif c == 'E':
            tb.append(1 / 3)
        elif c == '[':
            if len(tb) > 0:
                tb[-1] = tb[-1] + 0.5 * tb[-1]
        elif c == ']':
            if len(tb) > 0:
                if tb[-1] > float(1.0 / 1024):
                    tb[-1] = tb[-1] / 2
        elif c == '-':
            if len(tb) > 0:
                tb[-1] = -tb[-1]
        if len(tb) > 0:
            return tb[-1]
        else:
            return 1

    def is_duration_char(c: str):
        return c in ['A', 'B', 'C', 'D', 'E']

    str_arr = [c for c in string]
    tab = []
    while not len(str_arr) == 0:
        nb_chars_read = 1

        if str_arr[0] == '+' and len(str_arr) >= 2:
            nb_chars_read = 2
            if len(tab) > 0 and is_duration_char(str_arr[1]):
                old_read = tab[-1]
                new_read = char_to_duration(str_arr[1], tab)
                new_dur = fabs(old_read) + fabs(new_read)
                if old_read < 0:
                    new_dur = -new_dur
                tab[-2] = new_dur
                tab = tab[:-1]

        else:
            char_to_duration(str_arr[0], tab)

        str_arr = str_arr[nb_chars_read:]  # remove chars read
    return tab
