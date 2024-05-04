import itertools
from lib.constants import GAMMA
from lib.entity.ParseTreeNode import ParseTreeNode
from lib.parser.entity.Chart import Chart
from lib.parser.entity.ChartState import ChartState


def extract_tree_roots(chart: Chart):
    completedGammaState = chart.build_complete_gamma_state()
    return create_trees_for_state(chart, completedGammaState)


def create_trees_for_state(chart: Chart, state: ChartState):
    trees = []

    if state.is_terminal():
        trees.append(ParseTreeNode(
            state.rule.antecedent.predicate,
            [],
            state.rule.consequents[0].predicate,
            state.rule
        ))
    else:
        for child_state_permutation in find_child_state_sequences(chart, state):
            for permutation_trees in create_trees_for_states(chart, child_state_permutation):
                trees.append(ParseTreeNode(
                    state.rule.antecedent.predicate,
                    permutation_trees,
                    "",
                    state.rule
                ))

    return trees


def find_child_state_sequences(chart: Chart, parent_state: ChartState) -> list[list[ChartState]]:
    """
    Each state may have multiple sequences of possible children, find them.
    """
    return find_state_sequences(chart, parent_state, parent_state.end_word_index, len(parent_state.rule.consequents) - 1)


def find_state_sequences(chart: Chart, parent_state: ChartState, end_word_position: int, consequent_index: int):
    sequences = []
    for state in chart.completed_states[end_word_position]:
        if state.rule.antecedent.predicate == parent_state.rule.consequents[consequent_index].predicate:
            if consequent_index == 0:
                sequences.append([state])
            else:
                previous_sequences = find_state_sequences(chart, parent_state, state.start_word_index, consequent_index-1)
                for previous_sequence in previous_sequences:
                    previous_sequence.append(state)
                    sequences.append(previous_sequence)
    return sequences


def create_trees_for_states(chart: Chart, states: list[ChartState]) -> list[list[ParseTreeNode]]:
    # each state has multiple trees
    trees_per_state = [create_trees_for_state(chart, state) for state in states]
    # create all of their permutations
    return create_permutations(trees_per_state)


def create_permutations(things: list[list]) -> list[list]:
    """
    For a list [[a, b], [1, 2], [W, X]], create all permutations, like [a, 1, W] and [b, 1, X]
    See for example https://www.geeksforgeeks.org/python-all-possible-permutations-of-n-lists/
    """
    return list(itertools.product(*things))


# Returns the word that could not be parsed (or ""), and the index of the last completed word
def find_unknown_word(chart: Chart):
    """
    Returns the word that could not be parsed (or ""), and the index of the last completed word
    """

    nextWord = ""
    lastUnderstoodIndex = -1

    # for i = len(chart.states) - 1; i >= 0; i -= 1:
    for i in range(len(chart.states) - 1, -1, -1):
        states = chart.states[i]
        for state in states :
            if state.is_complete():
                if state.end_word_index > lastUnderstoodIndex:
                    lastUnderstoodIndex = state.end_word_index - 1

    if lastUnderstoodIndex+1 < len(chart.words):
        nextWord = chart.words[lastUnderstoodIndex+1]
    else:
        nextWord = " ".join(chart.words)

    return nextWord
