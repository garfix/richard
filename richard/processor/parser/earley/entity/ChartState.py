from dataclasses import dataclass
from richard.constants import TERMINAL
from richard.entity.GrammarRule import GrammarRule


class ChartState:

    rule: GrammarRule
    dot_position:    int
    start_word_index: int
    end_word_index:   int


    def __init__(self, rule: GrammarRule, dot_position: int, start_word_index: int, end_word_index: int) -> None:
        self.rule = rule
        self.dot_position = dot_position
        self.start_word_index = start_word_index
        self.end_word_index = end_word_index


    def __hash__(self) -> int:
        return hash((self.rule.hash, self.dot_position, self.start_word_index, self.end_word_index))
    
    
    def __eq__(self, other_state: object) -> bool:
        return self.rule.equals(other_state.rule) and \
               self.dot_position == other_state.dot_position and \
               self.start_word_index == other_state.start_word_index and \
               self.end_word_index == other_state.end_word_index
    

    def is_terminal(self):
        if len(self.rule.consequents[0].arguments) == 0:
            return False
        return self.rule.consequents[0].arguments[0] == TERMINAL


    def is_complete(self):
        return self.dot_position >= len(self.rule.consequents) + 1


    def to_string(self, chart):
        s = self.rule.antecedent.predicate + " ->"
        for i, consequent in enumerate(self.rule.consequents):
            if i + 1 == self.dot_position:
                s += " *"
            s += f" {consequent.predicate}"
        if len(self.rule.consequents) + 1 == self.dot_position:
            s += " *"

        s += " <"
        for i, word in enumerate(chart.words):
            if i >= self.start_word_index and i < self.end_word_index:
                s += f" {word}"
        s += " >"
        return s

