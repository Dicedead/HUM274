from L_system import *
from rand_rules import *

initial = "F-F-F-F"
rule = Rule("F", "F-F+F+FF-F-F+F")

rules = Rules(rule)
print(rules.run(initial, 2, show_mode=True))

##TODO mostly just translate L system to rhythm + superposer une ligne rythmique avec 4 lignes mélodiques (encodées comme
##tableaux d'ints + règle de conversion int <-> pitch)
