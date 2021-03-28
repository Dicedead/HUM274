from L_system import *


def rules_basic():
    rule_a = Rule("A", "BB+E")
    rule_b = Rule("B", "DE-C")
    rule_c = Rule("C", "CD+C--C--")
    rule_d = Rule("D", "AD--D-D-D-ED")
    rule_e = Rule("E", "E-B")
    return LSystem(rule_a, rule_b, rule_c, rule_d, rule_e)


def initial_beethov():
    return "EEEA+"


def run_basic_for(n, show_mode=False):
    return rules_basic().run(initial_beethov(), n, show_mode)


def rules_complex():
    rule_a = Rule("A", "BB[F+E-D+A]FF")
    rule_b = Rule("B", "D[E]-C""D[E]-C")
    rule_c = Rule("C", "CD+C-CF-")
    rule_d = Rule("D", "AE+[D-D]D+ED")
    rule_e = Rule("E", "[E+-]B")
    rule_f = Rule("F", "F+[-B]B[[A]EF]")
    return LSystem(rule_a, rule_b, rule_c, rule_d, rule_e, rule_f)


def initial_complex():
    return "[F]AEE-B"


def run_complex_for(n, show_mode=False):
    return rules_complex().run(initial_complex(), n, show_mode)
