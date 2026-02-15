from richard.entity.Variable import Variable


def unification(term1: any, term2: any, binding: dict) -> dict|None:
    if binding is None:
        return None

    # list: matches if either all atoms of term1 match with term2, or all atoms of term2 match with term1 (or both)
    if isinstance(term1, list) and isinstance(term2, list):
        binding = unify_lists(term1, term2, binding)
    # tuple
    elif isinstance(term1, tuple) and isinstance(term2, tuple):
        binding = unify_tuples(term1, term2, binding)
    # variables
    elif isinstance(term1, Variable) and isinstance(term2, Variable):
        binding = unify_variables(term1, term2, binding)
    # single variable
    elif isinstance(term2, Variable):
        binding = unify_bindings(binding, {term2.name: term1})
    elif isinstance(term1, Variable):
        binding = unify_bindings(binding, {term1.name: term2})
    # other
    elif term1 != term2:
        binding = None

    return binding


def unify_lists(term1: list, term2: list, binding: dict):
    matches1 = {}
    matches2 = {}
    for i2, a2 in enumerate(term2):
        for i1, a1 in enumerate(term1):
            sub = unification(a1, a2, binding)
            if sub is not None:
                matches1[i1] = True
                matches2[i2] = True
                binding = unify_bindings(binding, sub)
    if len(matches1) != len(term1) and len(matches2) != len(term2):
        binding = None

    return binding


def unify_tuples(term1: tuple, term2: tuple, binding: dict):
    if len(term1) != len(term2):
        binding = None
    else:
        for bound_arg, free_arg in zip(term1, term2):
            binding = unify_bindings(binding, unification(bound_arg, free_arg, binding))

    return binding


def unify_variables(term1: Variable, term2: Variable, binding: dict):
    deref1 = dereference(term1, binding)
    deref2 = dereference(term2, binding)

    if isinstance(deref1, Variable) and isinstance(deref2, Variable):
        if deref1.name == deref2.name:
            return binding
        # bind any one variable to the other
        binding = unify_bindings(binding, {deref1.name: deref2})
    elif isinstance(deref1, Variable):
        binding = unify_bindings(binding, {deref1.name: deref2})
    elif isinstance(deref2, Variable):
        binding = unify_bindings(binding, {deref2.name: deref1})
    else:
        binding = unification(deref1, deref2, binding)

    return binding


def dereference(term: Variable, binding: dict):
    value = term
    while isinstance(value, Variable) and value.name in binding:
        value = binding[value.name]

    return value


def unify_bindings(old_binding: dict, new_binding: dict) -> dict|None:
    if old_binding is None:
        return None
    if new_binding is None:
        return None

    for key, value in new_binding.items():
        if key in old_binding:
            if old_binding[key] != value:
                return None

    return old_binding | new_binding
