from richard.core.constants import E1, E2
from richard.entity.Variable import Variable

List1 = Variable('List')

def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'I understand'",
            "if": [('output_type', 'understand')],
        },
        {
            "syn": "s() -> 'Insufficient information'",
            "if": [('output_type', 'unknown')],
        },
        {
            "syn": "s() -> 'No, they are the same'",
            "if": [('output_type', 'no_same')],
        },
        {
            "syn": "s() -> 'No, part means proper subpart'",
            "if": [('output_type', 'no_subpart')],
        },
        {
            "syn": "s() -> 'No, but the reverse is sometimes true'",
            "if": [('output_type', 'reverse_sometimes')],
        },
        {
            "syn": "s() -> 'Sometimes'",
            "if": [('output_type', 'sometimes')],
        },
        {
            "syn": "s() -> 'Yes'",
            "if": [('output_type', 'yes')],
        },
        {
            "syn": "s() -> 'No'",
            "if": [('output_type', 'no')],
        },
        {
            "syn": "s() -> 'The above statement is impossible'",
            "if": [('output_type', 'impossible')],
        },
        {
            "syn": "s() -> 'The answer is' text(E1)",
            "if": [('output_type', 'count'), ('output_count', E1)],
        },
        {
            "syn": "s() -> 'How many' text(E1) 'per' text(E2)+'?'",
            "if": [('output_type', 'how_many'), ('output_how_many', E1, E2)],
        },
        {
            "syn": "s() -> 'Don\\'t know whether' text(E1) 'is part of' text(E2)",
            "if": [('output_type', 'dont_know_part_of'), ('output_dont_know_part_of', E1, E2)],
        },
        {
            "syn": "s() -> custom()",
            "post": lambda out: out.strip()
        },
        {
            "syn": "custom() -> just_left_of(E1)? just_right_of(E1)? right_of(E1)?",
            "if": [('output_type', 'location'), ('output_location', E1)],
        },
        {
            "syn": "just_left_of(E1) -> 'Just to the left of the' text(E2)+'.'",
            "if": [('just_left_of', E1, E2)],
        },
        {
            "syn": "just_right_of(E1) -> 'Just to the right of the' text(E2)+'.'",
            "if": [('just_left_of', E2, E1)],
        },
        {
            "syn": "right_of(E1) -> 'Somewhere to the right of the following ..' format(List)",
            "if": [('find_all', 'E2', [('somewhere_left_of', E2, E1)], List1)],
            "format": lambda elements: format_list(elements)
        },
    ]


def format_list(elements):
    return "(" + ", ".join(elements) + ")"
