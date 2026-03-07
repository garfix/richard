from richard.entity.Variable import Variable


def format_term(value: any, indent: str = "\n") -> str:
    """
    Formats nested lists, tuples and strings
    """
    if isinstance(value, tuple):
        text = indent + "("
        sep = ""
        for element in value:
            text += sep + format_term(element, indent + "    ")
            sep = ", "
        text += ")"
    elif isinstance(value, list):
        text = indent + "["
        for element in value:
            text += format_term(element, indent + "    ")
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

