
import re
from richard.constants import TERMINAL, CATEGORY_PROPER_NOUN, NO_SENTENCE, NOT_UNDERSTOOD, POS_TYPE_REG_EXP, POS_TYPE_RELATION, POS_TYPE_WORD_FORM, UNKNOWN_WORD
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.Log import Log
from richard.entity.ProcessResult import ProcessResult
from richard.entity.RuleConstituent import RuleConstituent
from richard.interface.SomeLogger import SomeLogger
from .entity.Chart import Chart
from .entity.ChartState import ChartState
from .tree_extract import extract_tree_roots
from .unknown_word import find_unknown_word


class EarleyParser:
    """ 
    An implementation of Earley's top-down chart parsing algorithm as described in
    "Speech and Language Processing" (first edition) - Daniel Jurafsky & James H. Martin (Prentice Hall, 2000)
    """

    log: SomeLogger

    def __init__(self, log: SomeLogger = Log(False)):
        self.log = log


    def parse(self, grammar_rules: GrammarRules, tokens: list[str]) -> ProcessResult:

        chart = self.buildChart(grammar_rules, tokens, "s", ["P"])

        rootNodes = extract_tree_roots(chart)
        error = ""
        error_args = []

        if len(rootNodes) == 0:

            nextWord = find_unknown_word(chart)

            if nextWord != "":
                error = UNKNOWN_WORD
                error_args = [nextWord]
            elif len(tokens) == 0:
                error = NO_SENTENCE
                error_args = []
            else:
                error = NOT_UNDERSTOOD
                error_args = []

        return ProcessResult(
            products=rootNodes,
            error_code=error,
            error_args=error_args,
        )
    

    def buildChart(self, grammar_rules: GrammarRules, words, rootCategory, rootVariables):
        """
        The body of Earley's algorithm
        """

        chart = Chart(words, rootCategory, rootVariables)
        wordCount = len(words)

        chart.enqueue(chart.build_incomplete_gamma_state(), 0)

        for i in range(wordCount + 1):

            j = 0
            while j < len(chart.states[i]):

                # a state is a is_complete entry in the chart (rule, dot_position, start_word_index, end_word_index)
                state = chart.states[i][j]

                # check if the entry is parsed completely
                if not state.is_complete():

                    # add all entries that have this abstract consequent as their antecedent
                    self.predict(grammar_rules, chart, state)

                    # if the current word in the sentence has this part-of-speech, then
                    # we add a completed entry to the chart (part-of-speech => word)
                    if i < wordCount:
                        self.scan(chart, state)
                else:

                    # proceed all other entries in the chart that have this entry's antecedent as their next consequent
                    self.complete(chart, state)

                j += 1

        return chart
    

    def predict(self, grammar_rules: GrammarRules, chart: Chart, state: ChartState):
        """
        Adds all entries to the chart that have the current consequent of $state as their antecedent.
        """

        consequentIndex = state.dot_position - 1
        nextConsequent = state.rule.consequents[consequentIndex]
        next_consequent_variables = state.rule.consequents[consequentIndex].arguments
        end_word_index = state.end_word_index

        if self.log.is_active():
            self.log.add_debug("predict", state.to_string(chart))

        for rule in grammar_rules.find_rules(nextConsequent.predicate, len(next_consequent_variables)) :

            predicted_state = ChartState(rule, 1, end_word_index, end_word_index)
            chart.enqueue(predicted_state, end_word_index)

            if self.log.is_active():
                self.log.add_debug("> predicted", predicted_state.to_string(chart))


    def scan(self, chart: Chart, state: ChartState):
        """
        If the current consequent in state (which non-abstract, like noun, verb, adjunct) is one
        of the parts of speech associated with the current word in the sentence,
        then a new, completed, entry is added to the chart: (cat => word)
        """

        next_consequent = state.rule.consequents[state.dot_position - 1]
        next_pos_type = state.rule.consequents[state.dot_position - 1].position_type
        next_variables = state.rule.consequents[state.dot_position - 1].arguments
        end_word_index = state.end_word_index
        end_word = chart.words[end_word_index]
        lex_item_found = False
        new_pos_type = POS_TYPE_RELATION

        if self.log.is_active():
            self.log.add_debug("scan", state.to_string(chart))

        if next_pos_type == POS_TYPE_REG_EXP:
            if re.match(next_consequent, end_word):
                lex_item_found = True
                new_pos_type = POS_TYPE_REG_EXP

        # proper noun
        if not lex_item_found and next_consequent == CATEGORY_PROPER_NOUN:
            lex_item_found = True

        # literal word form
        if not lex_item_found:
            if (next_consequent.predicate == end_word.lower()) and (len(next_variables) == 0):
                lex_item_found = True
                new_pos_type = POS_TYPE_WORD_FORM

        if lex_item_found:
            rule = GrammarRule(
                RuleConstituent(next_consequent.predicate, next_variables, new_pos_type),
                [RuleConstituent(end_word, [TERMINAL], POS_TYPE_WORD_FORM)],
                None
            )

            scanned_state = ChartState(rule, 2, end_word_index, end_word_index+1)
            chart.enqueue(scanned_state, end_word_index+1)

            if self.log.is_active():
                self.log.add_debug("> scanned", scanned_state.to_string(chart)+" "+end_word)


    def complete(self, chart: Chart, completed_state: ChartState):
        """
        This function is called whenever a state is complete.
        Its purpose is to advance other states.
        
        For example:
        - this state is NP -> noun, it has been completed
        - now proceed all other states in the chart that are waiting for an NP at the current position
        """

        completed_antecedent = completed_state.rule.antecedent.predicate

        if self.log.is_active():
            self.log.add_debug("complete", completed_state.to_string(chart))

        # index the completed state for fast lookup in the tree extraction phase
        chart.index_completed_state(completed_state)

        for charted_state in chart.states[completed_state.start_word_index] :

            dot_position = charted_state.dot_position
            rule = charted_state.rule

            if (dot_position > len(rule.consequents)) or (rule.consequents[dot_position-1].predicate != completed_antecedent):
                continue

            # check if the types match
            if charted_state.rule.consequents[dot_position-1].position_type != completed_state.rule.antecedent.position_type:
                continue

            # create a new state that is a dot-advancement of an older state
            advanced_state = ChartState(rule, dot_position+1, charted_state.start_word_index, completed_state.end_word_index)

            # enqueue the new state
            chart.enqueue(advanced_state, completed_state.end_word_index)

            if self.log.is_active():
                self.log.add_debug("> advanced", advanced_state.to_string(chart))
