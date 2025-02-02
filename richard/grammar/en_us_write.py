from richard.core.constants import E1, NO_SENTENCE, NOT_UNDERSTOOD, UNKNOWN_WORD


def get_en_us_write_grammar():
    return [
        {
            "syn": "s() -> 'Sorry, I don\\'t understand'",
            "if": [('output_type', NOT_UNDERSTOOD)]
        },
        {
            "syn": "s() -> 'No sentence given'",
            "if": [('output_type', NO_SENTENCE)]
        },
        {
            "syn": "s() -> 'Could not understand:' text(E1)",
            "if": [('output_type', UNKNOWN_WORD), ('output_unknown_word', E1)]
        },
    ]
