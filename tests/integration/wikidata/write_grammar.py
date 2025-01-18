from richard.core.constants import E1


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s(E1) -> text(E1)",
            "if": [('output_type', 'report'), ('output_report', E1)],
        }
    ]
