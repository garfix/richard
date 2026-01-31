# -- McPAM helper functions (p189) ------------------------------------------------------

from tests.unit.micro_pam.cd_functions import filler_role, header_cd, match
from tests.unit.micro_pam.lisp_functions import atom, consp, evaluate, get, minusp, numberp


def match_side(side, item, bindings: dict) -> dict:

    current_bindings = match(pattern_side(side), item, bindings)

    if current_bindings:
        if constraint_side(side):
            return evaluate(constraint_side(side), current_bindings)

    return current_bindings


def isa(type: str, cd: any):
    if numberp(cd):
        return False
    elif atom(cd):
        return isa_check(type, cd)
    else:
        if isa_check(type, header_cd(cd)):
            return True
        x = filler_role("type", cd)
        if x:
            return isa_check(type, header_cd(x))

    return False


def isa_check(type, x):
    return type == x
    # TODO: necessary? if so, how?
    # or type == get(x, "isa")


def pos_val(cd):
    if consp(cd):
        cd = cd[0]
        if numberp(cd):
            return not minusp(cd) and cd != 0

# For the following functions, take this example:

# [
#     [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
#     [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]]
# ],

# this is the lhs (left-hand side)
# [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
#
# and from this "side",
#
# ['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]]
# is the pattern, and
# ['pos-val', '?n']
# is the constraint (which is optional)


def lhs(rule):
    return rule[0]


def rhs(rule):
    return rule[1]


def pattern_side(side):
    return side[0]


def constraint_side(side):
    if len(side) > 1:
        return side[1][0]
    return None





