from richard.entity.Variable import Variable
from richard.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


def generate_variables(term: any, variable_generator: VariableGenerator, variable_map: dict):
    # list
    if isinstance(term, list):
        return [generate_variables(arg, variable_generator, variable_map) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        return tuple([generate_variables(arg, variable_generator, variable_map) for arg in term])
    # variable
    elif isinstance(term, Variable):
        if term.name in variable_map:
            return variable_map[term.name]
        else:
            v = Variable(variable_generator.next())
            variable_map[term.name] = v
            return v
    else:
        # just the value
        return term

def variablize(term):
    # list
    if isinstance(term, list):
        return [variablize(arg) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        return tuple([variablize(arg) for arg in term])
    # variable
    elif isinstance(term, str) and term[0:1] == "$":
        return Variable(term)
    else:
        # just the value
        return term