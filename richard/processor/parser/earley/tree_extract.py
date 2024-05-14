import itertools
from richard.entity.ParseTreeNode import ParseTreeNode
from .entity.Chart import Chart
from .entity.ChartState import ChartState


def extract_tree_roots(chart: Chart):

    gamma_state = chart.build_complete_gamma_state()
    if not gamma_state.end_word_index in chart.completed_states:
        return []
    
    gamma_nodes = create_trees_for_state(chart, gamma_state)
    return [gamma_node.children[0] for gamma_node in gamma_nodes]


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
        # the state has one or more child states. in fact, there can be multiple child state sequences
        for child_state_sequence in find_child_state_sequences(chart, state):
            # each child state can have multiple parse trees, built from its children; go through all permutations of these child state parse trees
            for permutation_trees in create_trees_for_states(chart, child_state_sequence):
                trees.append(ParseTreeNode(
                    state.rule.antecedent.predicate,
                    permutation_trees,
                    "",
                    state.rule
                ))

    return trees


def find_child_state_sequences(chart: Chart, parent_state: ChartState) -> list[list[ChartState]]:
    """
    each state may have multiple sequences of possible children, find them.
    """
    return find_state_sequences(chart, parent_state, parent_state.end_word_index, len(parent_state.rule.consequents) - 1)


def find_state_sequences(chart: Chart, parent_state: ChartState, end_word_position: int, consequent_index: int):
    """
    try to match the consequent_index'th consequent of parent_state to a new state, ending in the end_word_position
    and prepend the earlier states. this may result in multiple state sequences
    """
    sequences = []
    for state in chart.completed_states[end_word_position]:
        if state.rule.antecedent.equals(parent_state.rule.consequents[consequent_index]):
            if consequent_index == 0 and state.start_word_index == parent_state.start_word_index:
                sequences.append([state])
            else:
                # find one or more preceding sequences of this state
                for previous_sequence in find_state_sequences(chart, parent_state, state.start_word_index, consequent_index-1):
                    sequences.append(previous_sequence + [state])
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
