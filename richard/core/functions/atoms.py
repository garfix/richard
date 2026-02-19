from richard.core.functions.unification import dereference
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
        # return dereference(construct, binding)
        # bound?
        if construct.name in binding:
            # add variable value
            return bind_variables(binding[construct.name], binding)
            # return binding[construct.name]
        else:
            # non-bound variable
            return construct
    else:
        # just the value
        return construct


def map_arguments(formal_parameters: list[any], arguments: list[any], binding: dict, all_variables) -> dict|None:
    """
    Maps all variables of formal_parameters to their argument
    Checks if the constants in formal_parameters match their argument
    """

    # initialize with binding variables that do not affect this rule (but may be used later on)
    rule_binding = {key: value for (key, value) in binding.items() if key not in all_variables}

    for rule_argument, value in zip(formal_parameters, arguments):

        if isinstance(value, Variable) and value.name in binding:
            bound_value = binding[value.name]
            #bound_value = bind_variables(value, binding)
        else:
            bound_value = value

        if isinstance(rule_argument, Variable):
            # bind variable
            if isinstance(bound_value, Variable):
                # A = E1
                pass
            else:
                # A = 'john'
                # check for conflicts
                if rule_argument.name in rule_binding:
                    if rule_binding[rule_argument.name] != bound_value:
                        return None

                rule_binding[rule_argument.name] = bound_value
                # rule_binding[rule_argument.name] = bind_variables(bound_value, binding)
        else:
            if isinstance(bound_value, Variable):
                # 'john' = E1
                pass
            else:
                # 'john' = 'susan'
                # check for conflicts
                if bound_value != rule_argument:
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


def convert_tuple_results_to_bindings(predicate: str, results: list, dereferenced_arguments: list, binding: dict):
    """
    Converts results into a list of bindings
    If a result has some variable in different positions, make sure the values at the positions do not conflict
    Also checks if the result keeps to the restrictions provided by the input
    """
    checked_results = []
    for result in results:

        # result = bind_variables(result, binding)

        # extend the incoming binding
        checked_result = binding.copy()
        # check needed for a variable that occurs twice
        conflict = False

        # go through all arguments
        for i, arg in enumerate(dereferenced_arguments):

            if result[i] is None:
                continue
            # variable?
            elif isinstance(arg, Variable):
                # if the variable was bound in the input binding, check if the result matches its value
                if arg.name in binding:
                    if binding[arg.name] != result[i]:
                        raise Exception(f"Result of '{predicate}' doesn't match variable '{arg.name}': {binding[arg.name]} != {result[i]}")
                # check for conflict with previous same variable
                if arg.name in checked_result and checked_result[arg.name] != result[i]:
                    conflict = True
                    break
                # extend the binding
                checked_result[arg.name] = result[i]
            else:
                # check if the result matches the given input
                if arg != result[i]:
                    # indicates an error in the relation
                    raise Exception(f"Result of '{predicate}' doesn't match input value: {dereferenced_arguments} => {result}")

        if not conflict:
            checked_results.append(checked_result)

    return checked_results
