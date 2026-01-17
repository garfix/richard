from richard.entity.Variable import Variable


def format_value(value: any, indent: str = "\n") -> str:
    """
    Formats nested lists, tuples and strings
    """
    if isinstance(value, tuple):
        text = indent + "("
        sep = ""
        for element in value:
            text += sep + format_value(element, indent + "    ")
            sep = ", "
        text += ")"
    elif isinstance(value, list):
        text = indent + "["
        for element in value:
            text += format_value(element, indent + "    ")
        text += indent + "]"
    elif isinstance(value, str):
        text = "'" + value + "'"
    else:
        text = str(value)
    return text


def get_atom_variables(construct: any) -> list[str]:
    variables = set()
    if isinstance(construct, Variable):
        variables.add(construct.name)
    elif isinstance(construct, tuple) or isinstance(construct, list):
        for arg in construct:
            for v in get_atom_variables(arg):
                variables.add(v)

    return list(variables)


def get_atoms_variables(atoms: list[tuple]) -> list[str]:
    variables = set()
    for atom in atoms:
        for v in get_atom_variables(atom):
            variables.add(v)

    return list(variables)


def bind_variables(construct: any, binding: dict) -> list:
    # list
    if isinstance(construct, list):
        return [bind_variables(arg, binding) for arg in construct]
    # tuple
    elif isinstance(construct, tuple):
        return tuple([bind_variables(arg, binding) for arg in construct])
    # variable
    elif isinstance(construct, Variable):
        # bound?
        if construct.name in binding:
            # add variable value
            return binding[construct.name]
        else:
            # non-bound variable
            return construct
    else:
        # just the value
        return construct


def unification(term1: any, term2: any) -> dict|None:
    binding = {}
    # list
    if isinstance(term1, list) and isinstance(term2, list):
        found = False
        for a2 in term2:
            for a1 in term1:
                sub = unification(a1, a2)
                if sub is not None:
                    found = True
                    binding = unification_binding(binding, sub)
        if not found:
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

