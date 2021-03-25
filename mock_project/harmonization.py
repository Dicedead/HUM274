class chord:
    empty = (-1, -1, -1, -1)

    def __init__(self, b, t, a, s):
        self.b = b
        self.t = t
        self.a = a
        self.s = s


class Chord_tree:
    def __init__(self, root):
        self.root = root


class Node(Chord_tree):
    def __init__(self, root: chord, leaves):
        super().__init__(root)
        self.root = root
        self.leaves = leaves


class Leaf(Chord_tree):
    def __init__(self, root: chord):
        super().__init__(root)
        self.root = root


class Empty(Chord_tree):
    def __init(self):
        self.root = chord.empty


cm = chord(0, 3, 5, 8)  # differents accords

transition = {}  # transitions des accords avec plusieurs options


def starting_melody():
    S = []
    A = []
    T = []
    B = []
    return (B, T, A, S)


def chose(option):
    # chose from options
    return option(0)


def next_chord(actual: chord, next_b):  # chord ou (1,2,3,4)
    options = transition.get(chord)
    if options != None:
        return chose(options)
    else:
        calculate_chord


composition_table = Chord_tree(Node(cm, Empty))
