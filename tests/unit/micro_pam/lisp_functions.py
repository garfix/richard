# -- Lisp functions (p54) ------------------------------------------------------

def atom(cd):
    return isinstance(cd, str) or isinstance(cd, int) or isinstance(cd, float)


def consp(cd):
    return None if atom(cd) else cd


def evaluate(cd):
    if isinstance(cd, list):
        # example; may not be needed
        if cd[0] == "plus":
            return cd[1] + cd[2]

    return None


def get(object, property):
    # depends on the structure of an object (?)
    return object[property]


def minusp(cd):
    return cd < 0


def numberp(cd):
    return isinstance(cd, int) or isinstance(cd, float)


