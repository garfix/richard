from lib.constants import POS_TYPE_RELATION
from lib.entity.GrammarRule import GrammarRule
from lib.entity.RuleConstituent import RuleConstituent
from lib.parser.entity.ChartState import ChartState


class Chart:
    rootCategory: str
    rootVariables: list[str]
    words: list[str]
    states: list[list[ChartState]]

    # all states that were completed, by dot position
    completed_states: dict[int, list[ChartState]]

    def __init__(self, words: list[str], rootCategory: str, rootVariables: list[str]) -> None:
        self.rootCategory = rootCategory
        self.words = words
        self.rootVariables = rootVariables
        self.states = [[] for _ in range(len(words) + 1)]

        self.completed_states = {}
    
    def buildIncompleteGammaState(chart):
        return ChartState(
            GrammarRule(
                RuleConstituent("gamma", ["G"], POS_TYPE_RELATION),
                [RuleConstituent(chart.rootCategory, chart.rootVariables, POS_TYPE_RELATION)],
                lambda sem: sem,
            ),
            1, 0, 0)


    def buildCompleteGammaState(chart):
        return ChartState(
            GrammarRule(
                RuleConstituent("gamma", ["G"], POS_TYPE_RELATION),
                [RuleConstituent(chart.rootCategory, chart.rootVariables, POS_TYPE_RELATION)],
                lambda sem: sem,
            ),
            2, 0, len(chart.words))


    def appendState(chart, oldStates, newState):
        newStates = []
        for state in oldStates :
            newStates.append(state)
        newStates.append( newState)
        return newStates


    def enqueue(chart, state, position):
        found = chart.containsState(state, position)
        if not found:
            chart.pushState(state, position)

        return found


    def containsState(chart, state, position):
        for presentState in chart.states[position] :
            if presentState.equals(state):
                return True

        return False


    def pushState(chart, state, position):
        chart.states[position].append( state)

    
    def index_completed_state(self, completed_state: ChartState):
        if not completed_state.end_word_index in self.completed_states:
            self.completed_states[completed_state.end_word_index] = []
        self.completed_states[completed_state.end_word_index].append(completed_state)
