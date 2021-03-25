from L_system import *


def rules_abcde():
    rule_a = Rule("A", "BB+E")
    rule_b = Rule("B", "DE-C")
    rule_c = Rule("C", "CD+C--C--")
    rule_d = Rule("D", "AD--D-D-D-ED")
    rule_e = Rule("E", "E-B")
    return LSystem(rule_a, rule_b, rule_c, rule_d, rule_e)


def initial_abcde():
    return "EEEA+"


def run_abcde_for(n, show_mode=False):
    return rules_abcde().run(initial_abcde(), n, show_mode)
