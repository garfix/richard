from richard.entity.Variable import Variable


def unification(term1: any, term2: any) -> dict|None:

    binding = {}
    # list: matches if either all atoms of term1 match with term2, or all atoms of term2 match with term1 (or both)
    if isinstance(term1, list) and isinstance(term2, list):
        matches1 = {}
        matches2 = {}
        for i2, a2 in enumerate(term2):
            for i1, a1 in enumerate(term1):
                sub = unification(a1, a2)
                if sub is not None:
                    matches1[i1] = True
                    matches2[i2] = True
                    binding = unification_binding(binding, sub)
        if len(matches1) != len(term1) and len(matches2) != len(term2):
            binding = None
    # tuple
    elif isinstance(term1, tuple) and isinstance(term2, tuple):
        if len(term1) != len(term2):
            binding = None
        else:
            for bound_arg, free_arg in zip(term1, term2):
                binding = unification_binding(binding, unification(bound_arg, free_arg))
    # variable
    elif isinstance(term2, Variable):
        binding = unification_binding(binding, {term2.name: term1})
    elif isinstance(term1, Variable):
        binding = unification_binding(binding, {term1.name: term2})
    # other
    elif term1 != term2:
        binding = None

    return binding


def unification_binding(old_binding: dict, new_binding: dict) -> dict|None:
    if old_binding is None:
        return None
    if new_binding is None:
        return None

    for key, value in new_binding.items():
        if key in old_binding:
            if old_binding[key] != value:
                return None

    return old_binding | new_binding
