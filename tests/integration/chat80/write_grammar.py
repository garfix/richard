from richard.core.constants import E1, E2


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s(E1) -> 'OK'",
            "if": [('output_type', 'ok')],
        },
        {
            "syn": "s(E1) -> format(E1)",
            "if": [('output_type', 'list'), ('output_list', E1)],
            "format": lambda elements: ", ".join(elements),
        },
        {
            "syn": "s(E1) -> format(E1, E2)",
            "if": [('output_type', 'table'), ('output_table', E1, E2)],
            "format": lambda results, units: format_table(results, units),
        },
    ]


def format_table(table, units):
    response = sorted(table, key = lambda row: row[0])
    return response
