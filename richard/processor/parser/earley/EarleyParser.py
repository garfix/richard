import re
from richard.core.constants import DELTA, POS_TYPE_REG_EXP, ROOT_CATEGORY, TERMINAL, NO_SENTENCE, NOT_UNDERSTOOD, POS_TYPE_RELATION, POS_TYPE_WORD_FORM, UNKNOWN_WORD
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.ProcessResult import ProcessResult
from richard.entity.RuleConstituent import RuleConstituent
from .entity.Chart import Chart
from .entity.ChartState import ChartState
from .tree_extract import extract_tree_roots
from .unknown_word import find_unknown_word


class EarleyParser:
    """
    An implementation of Earley's top-down chart parsing algorithm as described in
    "Speech and Language Processing" (first edition) - Daniel Jurafsky & James H. Martin (Prentice Hall, 2000)
    """


    def parse(self, grammar_rules: GrammarRules, text: str) -> ProcessResult:

        chart = self.buildChart(grammar_rules, text)

        rootNodes = extract_tree_roots(chart)

        error = ""

        if len(rootNodes) == 0:

            nextWord = find_unknown_word(chart)

            if nextWord != "":
                error = UNKNOWN_WORD + " " + nextWord
            elif len(text) == 0:
                error = NO_SENTENCE
            else:
                error = NOT_UNDERSTOOD

        return ProcessResult(
            products=rootNodes,
            error=error
        )


    def buildChart(self, grammar_rules: GrammarRules, text: str):
        """
        The body of Earley's algorithm
        """

        chart = Chart(text)
        charCount = len(text)

        # gamma(G) -> delta(D)
        chart.enqueue(chart.build_incomplete_gamma_state(), 0)

        # delta(D) -> s(P1)
        # delta(D) -> s(P1, P2)
        # delta(D) -> s(P1, P2, P3)
        # ...
        for c in grammar_rules.find_argument_counts(ROOT_CATEGORY):
            variables = ["P" + str(j) for j in range(1, c+1)]
            grammar_rules.add_rule(GrammarRule(
                RuleConstituent(DELTA, ["D"], POS_TYPE_RELATION),
                [RuleConstituent(ROOT_CATEGORY, variables, POS_TYPE_RELATION)],
                sem=lambda s: s
            ))


        for i in range(charCount + 1):

            j = 0
            while j < len(chart.states[i]):

                # a state is a is_complete entry in the chart (rule, dot_position, start_char_index, end_char_index)
                state = chart.states[i][j]

                # check if the entry is parsed completely
                if not state.is_complete():

                    # add all entries that have this abstract consequent as their antecedent
                    self.predict(grammar_rules, chart, state)

                    # if the current token in the sentence has this part-of-speech, then
                    # we add a completed entry to the chart (part-of-speech => word)
                    if i < charCount:
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
        end_char_index = state.end_char_index

        for rule in grammar_rules.find_rules(nextConsequent.predicate, len(next_consequent_variables)) :

            predicted_state = ChartState(rule, 1, end_char_index, end_char_index)
            chart.enqueue(predicted_state, end_char_index)


    def scan(self, chart: Chart, state: ChartState):
        """
        If the current consequent in state (which non-abstract, like noun, verb, adjunct) is one
        of the parts of speech associated with the current word in the sentence,
        then a new, completed, entry is added to the chart: (cat => word)
        """

        next_consequent = state.rule.consequents[state.dot_position - 1]
        end_char_index = state.end_char_index

        # match a regular expression over multiple tokens
        if next_consequent.position_type == POS_TYPE_REG_EXP:
            word = self.perform_regexp(chart.text, end_char_index, next_consequent.predicate)
            if word is not None:
                for i in range(1, len(word)+1):
                    sub_word = word[0:i]
                    sem = self.create_semantic_function_for_scanned_state(sub_word)
# todo check if match regexp
                    self.add_scanned_state(chart, state, sub_word, sem)

        # match a string constant over multiple tokens
        if next_consequent.position_type == POS_TYPE_WORD_FORM:
            found = self.read_word(chart.text, end_char_index, next_consequent.predicate)
            if found:
                word = next_consequent.predicate
                self.add_scanned_state(chart, state, word, None)


    def create_semantic_function_for_scanned_state(self, word):
        return lambda: word


    def add_scanned_state(self, chart: Chart, state: ChartState, word: str, sem):
        next_consequent = state.rule.consequents[state.dot_position - 1]
        next_variables = state.rule.consequents[state.dot_position - 1].arguments
        end_char_index = state.end_char_index
        length = len(word)
        rule = GrammarRule(
            RuleConstituent(next_consequent.predicate, next_variables, next_consequent.position_type),
            [RuleConstituent(word, [TERMINAL], POS_TYPE_WORD_FORM)],
            sem,
        )

        scanned_state = ChartState(rule, 2, end_char_index, end_char_index+length)
        chart.enqueue(scanned_state, end_char_index+length)


    def complete(self, chart: Chart, completed_state: ChartState):
        """
        This function is called whenever a state is complete.
        Its purpose is to advance other states.

        For example:
        - this state is NP -> noun, it has been completed
        - now proceed all other states in the chart that are waiting for an NP at the current position
        """

        completed_antecedent = completed_state.rule.antecedent.predicate

        # index the completed state for fast lookup in the tree extraction phase
        chart.index_completed_state(completed_state)

        for charted_state in chart.states[completed_state.start_char_index]:

            dot_position = charted_state.dot_position
            rule = charted_state.rule

            if (dot_position > len(rule.consequents)) or (rule.consequents[dot_position-1].predicate != completed_antecedent):
                continue

            # check if the types match
            if charted_state.rule.consequents[dot_position-1].position_type != completed_state.rule.antecedent.position_type:
                continue

            # create a new state that is a dot-advancement of an older state
            advanced_state = ChartState(rule, dot_position+1, charted_state.start_char_index, completed_state.end_char_index)

            # enqueue the new state
            chart.enqueue(advanced_state, completed_state.end_char_index)


    def perform_regexp(self, text: str, start_index: int, regexp: str):
        part = text[start_index:]
        result = re.match(regexp, part)
        word = None
        if result:
            word = result.group(0)

        return word


    def read_word(self, text: str, start_index: int, word: str):
        part = text[start_index:].lower()
        return part[:len(word)] == word

