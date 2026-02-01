# -- Lisp functions (p54) ------------------------------------------------------

def atom(cd):
    return isinstance(cd, str) or isinstance(cd, int) or isinstance(cd, float)


def consp(cd):
    return None if atom(cd) else cd


def get(object, property):
    # depends on the structure of an object (?)
    return object[property]


def minusp(cd):
    return cd < 0


def numberp(cd):
    return isinstance(cd, int) or isinstance(cd, float)


