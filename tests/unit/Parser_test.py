import unittest

from richard.core.BasicGenerator import BasicGenerator
from richard.core.Model import Model
from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.core.constants import E1
from richard.entity.SentenceRequest import SentenceRequest
from richard.grammar.en_us_write import get_en_us_write_grammar
from richard.module.BasicOutputBuffer import BasicOutputBuffer
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser

class TestParser(unittest.TestCase):

    def test_rules_parser(self):

        tests = [
            {
                'rule': {"syn": "s(V) -> np(E1) vp(V, E1)"},
                'variants': [
                    "s(V) -> np(E1) ' ' vp(V, E1)",
                ]
            },
            {
                'rule': {"syn": "s(V) -> np(E1) + vp(V, E1)"},
                'variants': [
                    "s(V) -> np(E1) vp(V, E1)",
                ]
            },
            {
                'rule': {"syn": "s(V) -> np(E1) ~ vp(V, E1)"},
                'variants': [
                    "s(V) -> np(E1) ' ' vp(V, E1)",
                    "s(V) -> np(E1) vp(V, E1)",
                ]
            },
            {
                'rule': {"syn": "s(V) -> np(E1) 'too'? vp(V, E1)"},
                'variants': [
                    "s(V) -> np(E1) ' ' 'too' ' ' vp(V, E1)",
                    "s(V) -> np(E1) ' ' vp(V, E1)",
                ]
            },
            {
                'rule': {"syn": "s(V) -> np(E1)+'too'? vp(V, E1)"},
                'variants': [
                    "s(V) -> np(E1) 'too' ' ' vp(V, E1)",
                    "s(V) -> np(E1) ' ' vp(V, E1)",
                ]
            },
            {
                'rule': {"syn": "s(V) -> 'too'? np(E1) vp(V, E1)"},
                'variants': [
                    "s(V) -> 'too' ' ' np(E1) ' ' vp(V, E1)",
                    "s(V) -> np(E1) ' ' vp(V, E1)",
                ]
            },
        ]


        for test in tests:
            grammar = SimpleGrammarRulesParser().parse_read_grammar([test['rule']])
            rules = [str(rule) for rule in grammar.index['s'][1]]
            self.assertEqual(rules, test['variants'])


    def test_parser_process(self):

        simple_grammar = [
            { "syn": "s(V) -> np(E1) vp(V, E1)" },
            { "syn": "vp(V, E1) -> verb(V) np(E1)" },
            { "syn": "np(E1) -> noun(E1)" },
            { "syn": "noun(E1) -> proper_noun(E1)" },
            { "syn": "proper_noun(E1) -> 'john'" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'loves'" },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)

        system = System(
            input_pipeline=[
                FindOne(parser)
            ]
        )

        request = SentenceRequest("John loves Mary")
        parse_tree = system.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(john 'john'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'mary')))))")


    def test_quote(self):

        simple_grammar = [
            { "syn": "s(V) -> np(E1)+'\\''+'s' np(E2)" },
            { "syn": "np(E1) -> 'john'" },
            { "syn": "np(E1) -> 'shoe'" },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)

        system = System(
            input_pipeline=[
                FindOne(parser)
            ]
        )

        # note: two spaces
        request = SentenceRequest("John's  shoe")
        parse_tree = system.enter(request)

        self.assertEqual(parse_tree.inline_str(), "s(np(john 'john') ' ''' s 's' np(shoe 'shoe'))")


    def test_syntax_error(self):
        simple_grammar = [
            { "syn": "s(V) => proper_noun(E1) verb(V)" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'walks'" },
        ]

        try:
            grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
            parser = BasicParser(grammar)
        except Exception as e:
            self.assertEqual(str(e), "Missing -> operator in 'syn' value: s(V) => proper_noun(E1) verb(V)")


    def test_parse_error(self):
        simple_read_grammar = [
            { "syn": "s(V) -> proper_noun(E1) verb(V)" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'walks'" },
        ]

        output_buffer = BasicOutputBuffer()

        model = Model([
            output_buffer
        ])

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_read_grammar)
        parser = BasicParser(read_grammar)
        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_en_us_write_grammar())
        generator = BasicGenerator(write_grammar, model, output_buffer)

        system = System(
            model=model,
            input_pipeline=[
                FindOne(parser)
            ],
            output_generator=generator
        )

        request = SentenceRequest("Mary talks")
        system.enter(request)
        response = generator.generate_output()
        self.assertEqual(response, "Could not understand: talks ...")

