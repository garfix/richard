# -- McPAM helper functions (p189) ------------------------------------------------------

from tests.unit.micro_pam.cd_functions import filler_role, header_cd, match
from tests.unit.micro_pam.lisp_functions import atom, consp, evaluate, minusp, numberp


def match_side(side, item, bindings: dict) -> dict:
    current_bindings = match(pattern_side(side), item, bindings)
    # todo: strange: latest current_bd
    return current_bindings and evaluate(constraint_side(side)) and current_bindings


def isa(type: str, cd: any):
    if numberp(cd):
        return False
    elif atom(cd):
        return isa_check(type, cd)
    else:
        if isa_check(type, header_cd(cd)):
            return True
        x = filler_role("type", cd)
        if isa_check(type, header_cd, x):
            return True

    return False


def isa_check(type, x):
    return type == x or type == get(x, "isa")


def pos_val(cd):
    if consp(cd):
        cd = cd[0]
        if numberp(cd):
            return not minusp(cd) and cd != 0


def lhs(rule):
    return rule[0]


def rhs(rule):
    return rule[1]


def pattern_side(side):
    return side[0]


def constraint_side(side):
    if side[1]:
        return side[1][0]
    return None





