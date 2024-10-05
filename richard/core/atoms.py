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


def get_atom_variables(atom: tuple) -> list[str]:
    variables = set()
    for arg in atom:
        if isinstance(arg, Variable):
            variables.add(arg.name)
        elif isinstance(arg, list):
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


