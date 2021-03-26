"""
For the sake of simplicity, we will restrict ourselves to a simple harmonisation, with some assumptions:

The key will be C Major.
Each note of the bass line represents its corresponding grade in the key, hence each chord is in fundamental state,
i.e. there are no inversions.
The chords are only formed with fifths, i.e., we do not use seventh or ninth chords.

For the final project, we could implement a much more complex algorithm and objects in order to achieve a bigger variety
of better armonizations: we could establish less assumptions and add more rules.
"""

DO = 0
RE = 2
MI = 4
FA = 5
SOL = 7
LA = 9
SI = 11
OCTAVE = 12


class Chord:
    def __init__(self, b: int, t: int, a: int, s: int):
        self.b = b
        self.t = t
        self.a = a
        self.s = s

    def simplify(self):
        reduced = [self.b % 12, self.t % 12, self.a % 12, self.s % 12]
        return sorted(list(set(reduced)))

    def fundamental(self):
        return self.b

    def check_ranges(self):
        abs_range_b: bool = DO <= self.b <= DO + 2 * OCTAVE
        abs_range_t: bool = SOL <= self.t <= SOL + 2 * OCTAVE
        abs_range_a: bool = SOL + 1 * OCTAVE <= self.a <= MI + 3 * OCTAVE
        abs_range_s: bool = DO + 2 * OCTAVE <= self.s <= SOL + 3 * OCTAVE

        absolute_ranges: bool = abs_range_b and abs_range_t and abs_range_a and abs_range_s

        inter_ranges: bool = (self.s - self.a <= 9) and (self.a - self.t <= 9) and (self.t - self.b <= 15)

        return absolute_ranges and inter_ranges

    empty = __init__(-1, -1, -1, -1)


class SimplifiedChord:
    def __init__(self, fundamental: int, third: int, fifth: int):
        self.fundamental = fundamental
        self.third = third
        self.fifth: fifth

    Do = __init__(DO, MI, SOL)
    Re = __init__(RE, FA, LA)
    Mi = __init__(MI, SOL, SI)
    Fa = __init__(FA, LA, DO)
    Sol = __init__(SOL, SI, RE)
    La = __init__(LA, DO, MI)
    Si = __init__(SI, RE, FA)

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
    def of(fundamental: int):
        return SimplifiedChord.mapping.get(fundamental % 12, -1)


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
        super().__init__(Chord.empty, depth)


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
        next_chord = Chord.empty
        next_simple_chord = SimplifiedChord.of(next_note)

        ...


def compose(initial_chord: Chord, bass_line: list, empty_composition_tree: ChordTree):
    """
    Recursive function that from an initial chord, a bass line and an empty composition tree
    creates a composition tree with all the possible harmonizations.
    """


start_chord = Chord(0, 3, 5, 8)

Bass = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

transition = {}  # dictionary that includes transitions from a chord and a bass note to all the possibilities

compositionTree = Node(start_chord, 1, next_chords(start_chord))