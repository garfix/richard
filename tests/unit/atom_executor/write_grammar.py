from richard.core.constants import E1, E2


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'Name not found:' text(E1)",
            "if": [('output_type', 'name_not_found'), ('output_name_not_found', E1)],
        }
    ]
