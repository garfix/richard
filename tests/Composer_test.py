import unittest

from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.constants import E1, E2, EXISTS
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestComposer(unittest.TestCase):
   
    def test_missing_sem(self):
        grammar = [
            { "syn": "s(E1) -> proper_noun(E1) verb(V)", "sem": lambda proper_noun, verb: proper_noun + verb },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(E1) -> 'walks'" },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        exception_occurred = False
        try:
            pipeline.enter(SentenceRequest("Mary walks"))
        except Exception as e:
            self.assertEqual(str(e), "Rule 'proper_noun(E1) -> 'mary'' is missing key 'sem'")
            exception_occurred = True
        
        self.assertEqual(exception_occurred, True)


    def test_variable_unification(self):

        grammar = [
            { "syn": "s(E1) -> np(E1) vp(E1)", "sem": lambda np, vp: [('find', E1, np, vp)]},
            { "syn": "vp(E1) -> verb(E1, E2), np(E2)", "sem": lambda verb, np: [('find', E2, np, verb)] },
            { "syn": "verb(E1, E2) -> 'flows' 'to'", "sem": lambda: [('flow', E1, E2)] },
            { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: [('quant', E1, det, nbar)] },
            { "syn": "det(E1) -> 'the'", "sem": lambda: EXISTS },
            { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
            { "syn": "noun(E1) -> 'river'", "sem": lambda: [('river', E1)] },
            { "syn": "noun(E1) -> 'sea'", "sem": lambda: [('sea', E1)] },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        request = SentenceRequest("The river flows to the sea")
        pipeline.enter(request)
        composition = composer.get_composition(request)
        self.assertEqual(str(composition.semantics), "[('find', S1, [('quant', S1, 'exists', [('river', S1)])], [('find', S2, [('quant', S2, 'exists', [('sea', S2)])], [('flow', S1, S2)])])]")
        

    def test_special_category(self):

        grammar = [
            { "syn": "s(V) -> np(E1) 'sleeps'", "sem": lambda np: np },
            { "syn": "np(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },
            { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        request = SentenceRequest("John sleeps")
        pipeline.enter(request)

        tree = parser.get_tree(request)
        self.assertEqual(tree.inline_str(), "s(np(proper_noun(token 'John')) sleeps 'sleeps')")
        composition = composer.get_composition(request)
        self.assertEqual(str(composition.semantics), "John")

