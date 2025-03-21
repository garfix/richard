from .entity.Chart import Chart


# Returns the word that could not be parsed (or ""), and the index of the last completed word
def find_unknown_word(chart: Chart):
    """
    Returns the word that could not be parsed (or ""), and the index of the last completed word
    """

    nextWord = ""
    last_understood_index = -1

    # for i = len(chart.states) - 1; i >= 0; i -= 1:
    for i in range(len(chart.states) - 1, -1, -1):
        states = chart.states[i]
        for state in states :
            if state.is_complete():
                if state.end_char_index > last_understood_index:
                    last_understood_index = state.end_char_index - 1

    if last_understood_index+1 < len(chart.text):
        nextWord = chart.text[last_understood_index+1:last_understood_index+10] + " ..."
    else:
        nextWord = ""

    return nextWord
