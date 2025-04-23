from richard.core.constants import E1, E2


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'Hi there!'",
            "if": [('output_type', 'hi')],
        },
        {
            "syn": "s() -> format(E1)",
            "if": [('output_type', 'list'), ('output_list', E1)],
            "format": lambda elements: format_list(elements),
        },
    ]


def format_list(elements):
    elements.sort()
    return ", ".join(elements)

