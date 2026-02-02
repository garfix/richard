# -- McPAM helper functions (p189) ------------------------------------------------------

from tests.unit.micro_pam.lisp_functions import consp, minusp, numberp


def pos_val(cd):
    if consp(cd):
        cd = cd[0]
        if numberp(cd):
            return not minusp(cd) and cd != 0

# For the following functions, take this example:
#
# [
#     [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
#     [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]]
# ],
#
# this is the lhs (left-hand side)
#
# [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],

def lhs(rule):
    return rule[0]


def rhs(rule):
    return rule[1]

# and from this "side",
#
# ['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]]
#
# is the pattern, and
#
# ['pos-val', '?n']
#
# is the constraint (which is optional)

def pattern_side(side):
    return side[0]


def constraint_side(side):
    if len(side) > 1:
        return side[1]
    return None





