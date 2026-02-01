# -- CD functions (p63) --------------------------------------------------------

from tests.unit.micro_pam.extra_functions import get_variable_name, is_predication, is_predication_list, is_variable


def filler_role(role, cd):
    # looks for the pair (role filler) in the cd, and returns the filler
    # like this (?)
    for item in cd[1:]:
        if isinstance(item, list) and len(item) > 0 and item[0] == role:
            return item[1]

    return None


def header_cd(cd):
    # returns the main predicate of a cd form
    return cd[0]


def instantiate(pattern, bindings: dict):
    # binds pattern with bindings. if a variable can't be bound, it's set to NIL
    if isinstance(pattern, list):
        return [instantiate(element, bindings) for element in pattern]
    elif is_variable(pattern):
        variable = get_variable_name(pattern)
        if variable in bindings:
            return bindings[variable]
        else:
            return None
    else:
        return pattern


# NB! see p124: a predication that is in the pattern and not in the cd should match
def match(pattern, cd, bindings: dict):
    # if pattern matches cd, then the binding list is returned, with any new bindings added
    new_bindings = bindings.copy()
    if is_predication_list(pattern) and is_predication_list(cd):
        # each predication in pattern should match at least one in cd
        for p in pattern:
            found = False
            for c in cd:
                b = match(p, c, bindings)
                if b is not None:
                    found = True
                    new_bindings = merge_bindings(new_bindings, b)
                    break
            if not found:
                new_bindings = None
    elif is_predication(pattern) and is_predication(cd):
        # predicates should match
        if pattern[0] != cd[0]:
            new_bindings = None
        else:
            # each argument in the pattern should match one of the arguments in the cd
            for p in pattern[1:]:
                found = False
                for c in cd[1:]:
                    b = match(p, c, bindings)
                    if b is not None:
                        found = True
                        new_bindings = merge_bindings(new_bindings, b)
                        break
                if not found:
                    new_bindings = None
    elif is_variable(pattern):
        variable = get_variable_name(pattern)
        new_bindings = merge_bindings(new_bindings, {variable: cd})
    else:
        if pattern != cd:
            new_bindings = None

    return new_bindings


def merge_bindings(bindings1: dict, bindings2: dict) -> dict:
    if bindings1 is None or bindings2 is None:
        return None

    new_bindings = bindings1.copy()
    for key, value in bindings2.items():
        # check for conflict
        if key in bindings1 and bindings1[key] != bindings2[key]:
            return None
        # merge
        new_bindings[key] = value

    return new_bindings


