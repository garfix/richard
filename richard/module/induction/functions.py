from richard.entity.Variable import Variable


def instantiate(pattern, bindings: dict):
    # binds pattern with bindings. if a variable can't be bound, it's set to NIL
    if isinstance(pattern, list):
        return [instantiate(element, bindings) for element in pattern]
    elif isinstance(pattern< Variable):
        variable = pattern
        if variable in bindings:
            return bindings[variable]
        else:
            return None
    else:
        return pattern


def match(pattern, cd, bindings: dict):
    # if pattern matches cd, then the binding list is returned, with any new bindings added
    new_bindings = bindings.copy()
    if is_predication(pattern) and is_predication(cd):
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
        variable = pattern
        new_bindings = merge_bindings(new_bindings, {variable: cd})
    else:
        if pattern != cd:
            new_bindings = None

    return new_bindings
