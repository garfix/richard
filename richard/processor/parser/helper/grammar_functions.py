
from richard.type import SemanticTemplate


def apply(template: SemanticTemplate, *values):
    replaced = template.body
    for i, value in enumerate(values):
        token = template.args[i][0]       
        replaced = replace(replaced, token, value, True)

    return replaced


def replace(atoms, token, replacement, is_list):
    replaced = []
    for atom in atoms:
        if atom == token:
            replaced.extend(replacement)
        elif isinstance(atom, tuple):
            replaced.append(replace(atom, token, replacement, False))
        elif isinstance(atom, list):
            replaced.append(replace(atom, token, replacement, True))
        else:
            replaced.append(atom)

    return replaced if is_list else tuple(replaced)
