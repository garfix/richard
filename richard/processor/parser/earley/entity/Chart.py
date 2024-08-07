from richard.constants import GAMMA, POS_TYPE_RELATION
from richard.entity.GrammarRule import GrammarRule
from richard.entity.RuleConstituent import RuleConstituent
from richard.type.OrderedSet import OrderedSet
from .ChartState import ChartState


class Chart:
    root_category: str
    root_variables: list[str]
    words: list[str]
    states: list[OrderedSet[ChartState]]
    # all states that were completed, indexed by end word index
    completed_states: dict[int, list[ChartState]]


    def __init__(self, words: list[str], root_category: str, root_variables: list[str]) -> None:
        self.root_category = root_category
        self.words = words
        self.root_variables = root_variables
        self.states = [OrderedSet() for _ in range(len(words) + 1)]
        self.completed_states = {}

    
    def build_incomplete_gamma_state(chart):
        return ChartState(
            GrammarRule(
                RuleConstituent(GAMMA, ["G"], POS_TYPE_RELATION),
                [RuleConstituent(chart.root_category, chart.root_variables, POS_TYPE_RELATION)],
                None,
                [],
                [],
                0
            ),
            1, 0, 0)


    def build_complete_gamma_state(chart):
        return ChartState(
            GrammarRule(
                RuleConstituent(GAMMA, ["G"], POS_TYPE_RELATION),
                [RuleConstituent(chart.root_category, chart.root_variables, POS_TYPE_RELATION)],
                None,
                [],
                [],
                0
            ),
            2, 0, len(chart.words))


    def enqueue(chart, state, position):
        found = state in chart.states[position]
        if not found:
            chart.states[position].add(state)

        return found

    
    def index_completed_state(self, completed_state: ChartState):
        if not completed_state.end_word_index in self.completed_states:
            self.completed_states[completed_state.end_word_index] = []
        self.completed_states[completed_state.end_word_index].append(completed_state)
