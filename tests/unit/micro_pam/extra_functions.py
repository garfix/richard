# -- additional helper functions for the Python port ---------------------------

# ['person', ['name', 'John']]
def is_predication(cd):
    return isinstance(cd, list) and len(cd) > 1 and isinstance(cd[0], str)


# "?x"
def is_variable(cd):
    return isinstance(cd, str) and len(cd) > 0 and cd[0] == '?'


# [ ["name", "John"], ["profession", "barber"] ]
def is_predication_list(cd):
    return isinstance(cd, list) and len(cd) > 0 and is_predication(cd[0])


# "?x" => "x"
def get_variable_name(variable):
    return variable[1:]
