# -- Lisp functions (p54) ------------------------------------------------------

from tests.unit.micro_pam.cd_functions import instantiate
from tests.unit.micro_pam.extra_functions import is_predication


def atom(cd):
    return isinstance(cd, str) or isinstance(cd, int) or isinstance(cd, float)


def consp(cd):
    return None if atom(cd) else cd


def evaluate(cd, bindings: dict):
    if is_predication(cd):
        # example; may not be needed
        if cd[0] == "pos-val":
            value = instantiate(cd[1], bindings)
            return value > 0

    return None


def get(object, property):
    # depends on the structure of an object (?)
    return object[property]


def minusp(cd):
    return cd < 0


def numberp(cd):
    return isinstance(cd, int) or isinstance(cd, float)


