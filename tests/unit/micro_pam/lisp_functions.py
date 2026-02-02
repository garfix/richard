# -- Lisp functions (p54) ------------------------------------------------------

def atom(expression):
    # is expression an identifier, number or string?
    return isinstance(expression, str) or isinstance(expression, int) or isinstance(expression, float)


def consp(expression):
    # returns expression if not an atom, otherwise NIL
    return None if atom(expression) else expression


def minusp(expression):
    # is expression negative?
    return expression < 0


def numberp(expression):
    # is expression a number?
    return isinstance(expression, int) or isinstance(expression, float)
