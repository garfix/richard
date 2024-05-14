from richard.constants import GAMMA, POS_TYPE_RELATION
from richard.entity.GrammarRule import GrammarRule
from richard.entity.RuleConstituent import RuleConstituent
from .ChartState import ChartState


class Chart:
    root_category: str
    root_variables: list[str]
    words: list[str]
    states: list[list[ChartState]]
    # all states that were completed, indexed by end word index
    completed_states: dict[int, list[ChartState]]


    def __init__(self, words: list[str], root_category: str, root_variables: list[str]) -> None:
        self.root_category = root_category
        self.words = words
        self.root_variables = root_variables
        self.states = [[] for _ in range(len(words) + 1)]
        self.completed_states = {}

    
    def build_incomplete_gamma_state(chart):
        return ChartState(
            GrammarRule(
                RuleConstituent(GAMMA, ["G"], POS_TYPE_RELATION),
                [RuleConstituent(chart.root_category, chart.root_variables, POS_TYPE_RELATION)],
                None,
            ),
            1, 0, 0)


    def build_complete_gamma_state(chart):
        return ChartState(
            GrammarRule(
                RuleConstituent(GAMMA, ["G"], POS_TYPE_RELATION),
                [RuleConstituent(chart.root_category, chart.root_variables, POS_TYPE_RELATION)],
                None,
            ),
            2, 0, len(chart.words))


    def enqueue(chart, state, position):
        found = chart.contains_state(state, position)
        if not found:
            chart.states[position].append(state)

        return found


    def contains_state(chart, state, position):
        for present_state in chart.states[position] :
            if present_state.equals(state):
                return True

        return False        

    
    def index_completed_state(self, completed_state: ChartState):
        if not completed_state.end_word_index in self.completed_states:
            self.completed_states[completed_state.end_word_index] = []
        self.completed_states[completed_state.end_word_index].append(completed_state)
