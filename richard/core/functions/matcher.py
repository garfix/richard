from richard.entity.Variable import Variable


def match_induction_rule(antecedent_atoms: list[any], sentence_atoms: list[any]) -> list[dict]:
    bindings = match_induction_rule_rest(antecedent_atoms, sentence_atoms)
    return bindings


def match_induction_rule_rest(antecedent_atoms: list[any], sentence_atoms: list[any], binding: dict={}) -> list[dict]:
    if len(antecedent_atoms) == 0:
        return [binding]
    else:
        antecedent_atom = antecedent_atoms[0]
        new_bindings = match_induction_rule_atom(antecedent_atom, sentence_atoms, binding)
        results = []
        for new_binding in new_bindings:
            results.extend(match_induction_rule_rest(antecedent_atoms[1:], sentence_atoms, new_binding))

    return results


def match_induction_rule_atom(antecedent_atom: tuple, sentence_atoms: list[tuple], binding) -> list[dict]:
    results = []
    for sentence_atom in sentence_atoms:
        new_binding = match_atom(antecedent_atom, sentence_atom, binding)
        # print(antecedent_atom, sentence_atom, binding, new_binding)
        if new_binding is not None:
            results.append(new_binding)

    return results


def match_atom(formal_parameters: tuple, arguments: tuple, binding: dict) -> dict|None:

    new_binding = binding
    for formal_parameter, argument in zip(formal_parameters, arguments):
        term_binding = match_term(formal_parameter, argument, new_binding)
        if term_binding is None:
            return None
        new_binding = new_binding | term_binding

    return new_binding


def match_term(term1: any, term2: any, binding: dict) -> dict:
    # terms
    if isinstance(term1, tuple) and isinstance(term2, tuple):
        return match_atom(term1, term2, binding)
    # non-var / non-var
    if not isinstance(term1, Variable) and not isinstance(term2, Variable):
        return {} if term1 == term2 else None
    # var / non-var
    if isinstance(term1, Variable) and not isinstance(term2, Variable):
        return {term1.name: term2}
    # non-var / var
    if not isinstance(term1, Variable) and isinstance(term2, Variable):
        return {}
    # var / var
    if isinstance(term1, Variable) and isinstance(term2, Variable):
        return match_variable(term1, term2, binding)
    raise Exception("Unhandled case")


def match_variable(var1: Variable, var2: Variable, binding: dict):
    if var1.name in binding:
        if binding[var1.name] == var2:
            return {}
    else:
        return {var1.name: var2}
