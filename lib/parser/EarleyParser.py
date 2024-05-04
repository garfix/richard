
import re
from lib.constants import TERMINAL, CATEGORY_PROPER_NOUN, NO_SENTENCE, NOT_UNDERSTOOD, POS_TYPE_REG_EXP, POS_TYPE_RELATION, POS_TYPE_WORD_FORM, UNKNOWN_WORD
from lib.entity.GrammarRule import GrammarRule
from lib.entity.GrammarRules import GrammarRules
from lib.entity.Log import Log
from lib.entity.ParseResult import ParseResult
from lib.entity.ParseTreeNode import ParseTreeNode
from lib.entity.RuleConstituent import RuleConstituent
from lib.parser.entity.Chart import Chart
from lib.parser.entity.ChartState import ChartState
from lib.parser.tree_extract import extract_tree_roots, find_unknown_word


class EarleyParser:
    """ 
    An implementation of Earley's top-down chart parsing algorithm as described in
    "Speech and Language Processing" (first edition) - Daniel Jurafsky & James H. Martin (Prentice Hall, 2000)
    """

    grammarRules: GrammarRules
    log: Log

    def __init__(self, grammarRules: GrammarRules, log: Log):
        self.grammarRules = grammarRules
        self.log = log


    def parse(self, words: list[str], rootCategory: str, rootVariables: list[str]) -> list[ParseTreeNode]:
        """
        Parses words using EarleyParser.grammar
        Returns parse tree roots
        """

        chart = self.buildChart(self.grammarRules, words, rootCategory, rootVariables)

        rootNodes = extract_tree_roots(chart)
        error = ""
        errorArg = ""

        if len(rootNodes) == 0:

            nextWord = find_unknown_word(chart)

            if nextWord != "":
                error = UNKNOWN_WORD
                errorArg = nextWord
            elif len(words) == 0:
                error = NO_SENTENCE
                errorArg = ""
            else:
                error = NOT_UNDERSTOOD
                errorArg = ""

        result = ParseResult(
            root_nodes=rootNodes,
            error=error,
            error_arg=errorArg,
        )

        return rootNodes, result

    def buildChart(self, grammarRules: GrammarRules, words, rootCategory, rootVariables):
        """
        The body of Earley's algorithm
        """

        chart = Chart(words, rootCategory, rootVariables)
        wordCount = len(words)

        chart.enqueue(chart.buildIncompleteGammaState(), 0)

        for i in range(wordCount + 1):

            j = 0
            while j < len(chart.states[i]):

                # a state is a is_complete entry in the chart (rule, dot_position, start_word_index, end_word_index)
                state = chart.states[i][j]

                # check if the entry is parsed completely
                # print(state)
                if not state.is_complete():

                    # add all entries that have this abstract consequent as their antecedent
                    self.predict(grammarRules, chart, state)

                    # if the current word in the sentence has this part-of-speech, then
                    # we add a completed entry to the chart (part-of-speech => word)
                    if i < wordCount:
                        self.scan(chart, state)
                else:

                    # proceed all other entries in the chart that have this entry's antecedent as their next consequent
                    self.complete(chart, state)

                j += 1

        return chart

    def predict(self, grammarRules: GrammarRules, chart: Chart, state: ChartState):
        """
        Adds all entries to the chart that have the current consequent of $state as their antecedent.
        """

        consequentIndex = state.dot_position - 1
        nextConsequent = state.rule.consequents[consequentIndex]
        nextConsequentVariables = state.rule.consequents[consequentIndex].arguments
        end_word_index = state.end_word_index

        if self.log.is_active():
            self.log.add_debug("predict", state.to_string(chart))

        for rule in grammarRules.find_rules(nextConsequent.predicate, len(nextConsequentVariables)) :

            predictedState = ChartState(rule, 1, end_word_index, end_word_index)
            chart.enqueue(predictedState, end_word_index)

            if self.log.is_active():
                self.log.add_debug("> predicted", predictedState.to_string(chart))

    def scan(self, chart: Chart, state: ChartState):
        """
        If the current consequent in state (which non-abstract, like noun, verb, adjunct) is one
        of the parts of speech associated with the current word in the sentence,
        then a new, completed, entry is added to the chart: (cat => word)
        """

        nextConsequent = state.rule.consequents[state.dot_position - 1]
        nextPosType = state.rule.consequents[state.dot_position - 1].positionType
        nextVariables = state.rule.consequents[state.dot_position - 1].arguments
        end_word_index = state.end_word_index
        endWord = chart.words[end_word_index]
        lexItemFound = False
        newPosType = POS_TYPE_RELATION

        if self.log.is_active():
            self.log.add_debug("scan", state.to_string(chart))

        if nextPosType == POS_TYPE_REG_EXP:
            if re.match(nextConsequent, endWord):
                lexItemFound = True
                newPosType = POS_TYPE_REG_EXP

        # proper noun
        if not lexItemFound and nextConsequent == CATEGORY_PROPER_NOUN:
            lexItemFound = True

        # literal word form
        if not lexItemFound:
            if (nextConsequent.predicate == endWord.lower()) and (len(nextVariables) == 0):
                lexItemFound = True
                newPosType = POS_TYPE_WORD_FORM

        if lexItemFound:
            rule = GrammarRule(
                RuleConstituent(nextConsequent.predicate, nextVariables, newPosType),
                [RuleConstituent(endWord, [TERMINAL], POS_TYPE_WORD_FORM)],
                lambda sem: sem
            )

            scannedState = ChartState(rule, 2, end_word_index, end_word_index+1)
            chart.enqueue(scannedState, end_word_index+1)

            if self.log.is_active():
                self.log.add_debug("> scanned", scannedState.to_string(chart)+" "+endWord)

    def complete(self, chart: Chart, completedState: ChartState):
        """
        This function is called whenever a state is completed.
        Its purpose is to advance other states.
        //
        For example:
        - this state is NP -> noun, it has been completed
        - now proceed all other states in the chart that are waiting for an NP at the current position
        """

        completedAntecedent = completedState.rule.antecedent.predicate

        if self.log.is_active():
            self.log.add_debug("complete", completedState.to_string(chart))

        # index the completed state for fast lookup in the tree extraction phase
        chart.index_completed_state(completedState)

        for chartedState in chart.states[completedState.start_word_index] :

            dot_position = chartedState.dot_position
            rule = chartedState.rule

            if (dot_position > len(rule.consequents)) or (rule.consequents[dot_position-1].predicate != completedAntecedent):
                continue

            # check if the types match
            if chartedState.rule.consequents[dot_position-1].positionType != completedState.rule.antecedent.positionType:
                continue

            # create a new state that is a dot-advancement of an older state
            advancedState = ChartState(rule, dot_position+1, chartedState.start_word_index, completedState.end_word_index)

            # enqueue the new state
            chart.enqueue(advancedState, completedState.end_word_index)

            if self.log.is_active():
                self.log.add_debug("> advanced", advancedState.to_string(chart))
