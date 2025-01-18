from richard.core.constants import E1


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s(E1) -> 'OK'",
            "if": [('output_type', 'ok')],
        },
        {
            "syn": "s(E1) -> 'True'",
            "if": [('output_type', 'true')],
        },
        {
            "syn": "s(E1) -> 'False'",
            "if": [('output_type', 'false')],
        },
        {
            "syn": "s(E1) -> 'Unable to answer'",
            "if": [('output_type', 'unknown')],
        },
    ]
