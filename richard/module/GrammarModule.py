from richard.entity.GrammarRules import GrammarRules
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.entity.ExecutionContext import ExecutionContext


class GrammarModule(SomeModule):
    """
    This module contains predicates to extend the grammar
    """

    grammar: GrammarRules

    def __init__(self, grammar: GrammarRules) -> None:
        super().__init__()
        self.add_relation(Relation("learn_grammar_rule", query_function=self.learn_grammar_rule))
        self.grammar = grammar


    # ('learn_grammar_rule', simple_rule)
    def learn_grammar_rule(self, values: list, context: ExecutionContext) -> list[list]:
        simple_rule = values[0]

        rule = SimpleGrammarRulesParser().parse_simple_rule(simple_rule)
        self.grammar.add_rule(rule)

        return [
            [None]
        ]

