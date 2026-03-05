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


def has_variables(term: any) -> bool:
    return len(get_variables(term)) > 0


def get_variables(term: any) -> list[str]:
    variables = set()
    if isinstance(term, Variable):
        variables.add(term.name)
    elif isinstance(term, tuple) or isinstance(term, list):
        for arg in term:
            for v in get_variables(arg):
                variables.add(v)

    return list(variables)


def get_atoms_variables(atoms: list[tuple]) -> list[str]:
    variables = set()
    for atom in atoms:
        for v in get_variables(atom):
            variables.add(v)

    return list(variables)


def contains_variables(atoms: list):
    return len(get_atoms_variables(atoms)) > 0


def bind_variables(term: any, binding: dict) -> any:
    """
    Binds all variables in term to their binding from bindings
    Note: bindings may in turn contain variables, and these are bound as well
    """
    # list
    if isinstance(term, list):
        return [bind_variables(arg, binding) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        return tuple([bind_variables(arg, binding) for arg in term])
    # variable
    elif isinstance(term, Variable):
        # bound?
        if term.name in binding:
            # return the value, and try to bind it even further
            return bind_variables(binding[term.name], binding)
        else:
            # non-bound variable
            return term
    else:
        # just the value
        return term


def create_argument_binding(formal_parameters: list[any], arguments: list[any], binding: dict) -> dict|None:
    """
    Maps all variables of formal_parameters to their argument
    Checks if the constants in formal_parameters match their argument
    """
    rule_binding = {}

    for formal_parameter, value in zip(formal_parameters, arguments):

        bound_value = bind_variables(value, binding)

        if isinstance(formal_parameter, Variable):
            # bind variable
            if isinstance(bound_value, Variable):
                # A = E1
                pass
            else:
                # A = 'john'
                # check for conflicts
                if formal_parameter.name in rule_binding:
                    if rule_binding[formal_parameter.name] != bound_value:
                        return None

                rule_binding[formal_parameter.name] = bound_value
        else:
            if isinstance(bound_value, Variable):
                # 'john' = E1
                pass
            else:
                # 'john' = 'susan'
                # check for conflicts
                if bound_value != formal_parameter:
                    return None

    return rule_binding


def reify_variables(construct: any) -> any:
    """
    Returns a copy of construct with all variables it contains replaced by their names
    """
    # list
    if isinstance(construct, list):
        return [reify_variables(arg) for arg in construct]
    # tuple
    elif isinstance(construct, tuple):
        return tuple([reify_variables(arg) for arg in construct])
    # variable
    elif isinstance(construct, Variable):
        # return the name of the variable as an id
        return construct.name
    else:
        # just the value
        return construct

