from richard.core.constants import E1


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [('output_type', 'ok')],
        },
        {
            "syn": "s() -> 'True'",
            "if": [('output_type', 'true')],
        },
        {
            "syn": "s() -> 'False'",
            "if": [('output_type', 'false')],
        },
        {
            "syn": "s() -> 'Unable to answer'",
            "if": [('output_type', 'unknown')],
        },
    ]
