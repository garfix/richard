from richard.core.constants import E1, E2


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s(E1) -> 'I understand'",
            "if": [('output_type', 'understand')],
        },
        {
            "syn": "s(E1) -> 'Insufficient information'",
            "if": [('output_type', 'unknown')],
        },
        {
            "syn": "s(E1) -> 'No, they are the same'",
            "if": [('output_type', 'no_same')],
        },
        {
            "syn": "s(E1) -> 'No, part means proper subpart'",
            "if": [('output_type', 'no_subpart')],
        },
        {
            "syn": "s(E1) -> 'No, but the reverse is sometimes true'",
            "if": [('output_type', 'reverse_sometimes')],
        },
        {
            "syn": "s(E1) -> 'Sometimes'",
            "if": [('output_type', 'sometimes')],
        },
        {
            "syn": "s(E1) -> 'Yes'",
            "if": [('output_type', 'yes')],
        },
        {
            "syn": "s(E1) -> 'No'",
            "if": [('output_type', 'no')],
        },
        {
            "syn": "s(E1) -> 'The above statement is impossible'",
            "if": [('output_type', 'impossible')],
        },
        {
            "syn": "s(E1) -> 'The answer is' text(E1)",
            "if": [('output_type', 'count'), ('output_count', E1)],
        },
        {
            "syn": "s(E1) -> 'How many' text(E1) 'per' text(E2)+'?'",
            "if": [('output_type', 'how_many'), ('output_how_many', E1, E2)],
        },
        {
            "syn": "s(E1) -> 'Don\\'t know whether' text(E1) 'is part of' text(E2)",
            "if": [('output_type', 'dont_know_part_of'), ('output_dont_know_part_of', E1, E2)],
        },
    ]
