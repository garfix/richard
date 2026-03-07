from richard.core.functions.terms import bind_variables
from richard.core.functions.matcher import match_atom
from richard.entity.Variable import Variable


def tuple_results_to_bindings(predicate: str, arguments: list, results: list, binding: dict) -> list[dict]:
    """
    Converts results into a list of bindings
    If a result has some variable in different positions, make sure the values at the positions do not conflict
    Also checks if the result keeps to the restrictions provided by the input
    """

    checked_results = []
    for result in results:
        checked_result = match_atom(arguments, result, binding)
        if checked_result is not None:
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
                result.append(bind_variables(value, solution))

        results.append(result)

    return results
