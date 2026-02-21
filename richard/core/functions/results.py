from richard.entity.Variable import Variable


def tuple_results_to_bindings(predicate: str, arguments: list, results: list, binding: dict) -> list[dict]:
    """
    Converts results into a list of bindings
    If a result has some variable in different positions, make sure the values at the positions do not conflict
    Also checks if the result keeps to the restrictions provided by the input
    """
    checked_results = []
    for result in results:

        # extend the incoming binding
        checked_result = binding.copy()
        # check needed for a variable that occurs twice
        conflict = False

        # go through all arguments
        for arg, result_arg in zip(arguments, result):

            # None is defined as equal to input argument
            if result_arg is None:
                continue

            # variable?
            elif isinstance(arg, Variable):
                # results should not be variable
                if isinstance(result_arg, Variable):
                    raise Exception(f"Result of '{predicate}' contains a variable: {result}")
                # check for conflict with a previous result argument
                elif arg.name in checked_result and checked_result[arg.name] != result_arg:
                    # conflict: this result is excluded
                    conflict = True
                else:
                    # extend the binding
                    checked_result[arg.name] = result_arg
            else:
                # check if the result matches the given input
                if arg != result_arg:
                    # indicates an error in the relation
                    raise Exception(f"Result of '{predicate}' doesn't match input value: {arguments} => {result}")

        if not conflict:
            checked_results.append(checked_result)

    return checked_results


def bindings_to_tuple_results(formal_parameters: list, arguments: list, bindings: dict) -> list[list]:
    results = []

    for solution in bindings:

        result = []

        for formal_parameter, value in zip(formal_parameters, arguments):
            if isinstance(value, Variable):
                if isinstance(formal_parameter, Variable):
                    # check if the results are not bound (completely)
                    # this happens when r(X). is matches against r(Y).
                    if not formal_parameter.name in solution:
                        return []
                    result.append(solution[formal_parameter.name])
                else:
                    result.append(formal_parameter)
            else:
                result.append(value)

        results.append(result)

    return results
