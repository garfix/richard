from richard.core.functions.atoms import bind_variables
from richard.core.functions.matcher import match_induction_rule
from richard.entity.Variable import Variable


def instantiate(pattern, bindings: dict):
    # binds pattern with bindings. if a variable can't be bound, it's set to NIL
    if isinstance(pattern, list):
        return [instantiate(element, bindings) for element in pattern]
    elif isinstance(pattern, Variable):
        variable = pattern
        if variable in bindings:
            return bindings[variable]
        else:
            return None
    else:
        return pattern


def match(pattern, sentence, binding: dict):
    bound_pattern = bind_variables(pattern, binding)
    results = match_induction_rule(bound_pattern, sentence)
    return results[0] if len(results) > 0 else None
