class Rule:
    """
    Encodes L Systems' replacement rules.
    """

    def __init__(self, base: str, replacement: str):
        """
        :param base: string,
        :param replacement: string
        """
        self.base = base
        self.replacement = replacement


class LSystem:
    """
    L System's functionality.
    """

    def __init__(self, *rules):
        """
        An L System = a set of rules

        :param rules: List[Rule]
        """
        self.rules = {}
        [self.rules.update({rule.base: rule.replacement}) for rule in rules]

    def replace(self, base, show_mode: bool = False):
        """
        The brains of an L System, doing the simple task of applying each rule recursively

        :param base: some base string
        :param show_mode: boolean deciding whether to put separating brackets or not between rule applications
        :return: result of applications of all replacement rules on base string
        """
        new_string = ""
        for c in base:
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
        """
        Applies the replace method nb_iterations times with base string initial

        :param initial: first base string
        :param nb_iterations: how many times rules replacements should occur
        :param show_mode: boolean deciding whether to put separating brackets or not between rule applications
        :return: last result of rule applications
        """
        string = initial
        for i in range(nb_iterations):
            string = self.replace(string, show_mode)
        return string
