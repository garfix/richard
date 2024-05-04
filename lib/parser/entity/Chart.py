from lib.constants import POS_TYPE_RELATION
from lib.entity.GrammarRule import GrammarRule
from lib.entity.RuleConstituent import RuleConstituent
from lib.parser.entity.ChartState import ChartState


class Chart:
    rootCategory: str
    rootVariables: list[str]
    words: list[str]
    states: list[list[ChartState]]
    advanced: dict[str, list[list[ChartState]]]
    completed: dict[str, list[list[ChartState]]]

    def __init__(self, words: list[str], rootCategory: str, rootVariables: list[str]) -> None:
        self.rootCategory = rootCategory
        self.words = words
        self.rootVariables = rootVariables
        self.states = [[] for _ in range(len(words) + 1)]
        self.advanced = {}
        self.completed = {}
    
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

    def updateAdvancedStatesIndex(chart, completedState, advancedState):

        canonical = advancedState.start_form()
        completedConsequentsCount = advancedState.dot_position - 2

        if not canonical in chart.advanced:
            chart.advanced[canonical] = []

        children = []
        if completedConsequentsCount == 0:
            children = [completedState]
            chart.addAdvancedStateIndex(advancedState, children)
        else:
            for previousChildren in chart.advanced[canonical] :
                if len(previousChildren) == completedConsequentsCount:
                    if previousChildren[len(previousChildren)-1].end_word_index == completedState.start_word_index:
                        children = chart.appendState(previousChildren, completedState)
                        chart.addAdvancedStateIndex(advancedState, children)


    def addAdvancedStateIndex(chart, advancedState, children):
        canonical = advancedState.start_form()
        chart.advanced[canonical].append( children)

        if advancedState.is_complete():
            chart.updateCompletedStatesIndex(advancedState, children)


    def updateCompletedStatesIndex(chart, advancedState, children):

        canonical = advancedState.basic_form()

        if not canonical in chart.completed:
            chart.completed[canonical] = []

        chart.completed[canonical].append( children)


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

    