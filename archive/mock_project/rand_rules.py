import random


class RandomRules:
    def __init__(self, rules):
        self.rules = rules

    def replace(self, string):
        new_string = ""
        for c in string:
            new_list = [rule for rule in self.rules if rule.base == c]
            if new_list:
                new_string += random.choice(new_list).replacement
            else:
                new_string += c
        return new_string
