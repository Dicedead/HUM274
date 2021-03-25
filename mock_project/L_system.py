class Rule:

    """
    base: string,
    replacement: string
    """

    def __init__(self, base: str, replacement: str):
        self.base = base
        self.replacement = replacement


class Rules:

    """
    rules: List[Rule]
    """

    def __init__(self, *rules):
        self.rules = {}
        [self.rules.update({rule.base: rule.replacement}) for rule in rules]

    def replace(self, string, show_mode: bool = False):
        new_string = ""
        for c in string:
            if c in self.rules:
                if show_mode:
                    new_string += "<"
                new_string += self.rules.get(c)
                if show_mode:
                    new_string += ">"
            else:
                new_string += c
        return new_string

    def run(self, initial: str, nb_iterations: int, show_mode: bool = False):
        string = initial
        for i in range(nb_iterations):
            string = self.replace(string, show_mode)
        return string
