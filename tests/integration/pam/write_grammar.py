from richard.core.constants import E1, E2


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [('output_type', 'understood')],
        },
        {
            "syn": "s() -> 'Dunno'",
            "if": [('output_type', 'question')],
        },
    ]
