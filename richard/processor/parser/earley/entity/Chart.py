from richard.core.constants import DELTA, GAMMA, POS_TYPE_RELATION
from richard.entity.GrammarRule import GrammarRule
from richard.entity.RuleConstituent import RuleConstituent
from richard.type.OrderedSet import OrderedSet
from .ChartState import ChartState


class Chart:
    root_category: str
    root_variables: list[str]
    text: str
    states: list[OrderedSet[ChartState]]
    # all states that were completed, indexed by end char index
    completed_states: dict[int, list[ChartState]]


    def __init__(self, text: str) -> None:
        self.text = text
        self.states = [OrderedSet() for _ in range(len(text) + 1)]
        self.completed_states = {}


    def build_incomplete_gamma_state(self):
        return ChartState(
            GrammarRule(
                RuleConstituent(GAMMA, ["G"], POS_TYPE_RELATION),
                [RuleConstituent(DELTA, ["D"], POS_TYPE_RELATION)],
            ),
            1, 0, 0)


    def build_complete_gamma_state(self):
        return ChartState(
            GrammarRule(
                RuleConstituent(GAMMA, ["G"], POS_TYPE_RELATION),
                [RuleConstituent(DELTA, ["D"], POS_TYPE_RELATION)],
            ),
            2, 0, len(self.text))


    def enqueue(self, state: ChartState, position: int):
        found = state in self.states[position]
        if not found:
            self.states[position].add(state)

        return found


    def index_completed_state(self, completed_state: ChartState):
        if not completed_state.end_char_index in self.completed_states:
            self.completed_states[completed_state.end_char_index] = []
        self.completed_states[completed_state.end_char_index].append(completed_state)
