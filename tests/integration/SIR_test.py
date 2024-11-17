import unittest

from richard.block.TryFirst import TryFirst
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.module.GrammarModule import GrammarModule
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.store.MemoryDb import MemoryDb
from tests.integration.sir.SIRModule import SIRModule
from tests.integration.sir.SIRSentenceContext import SIRSentenceContext
from .sir.grammar import get_grammar


class TestSIR(unittest.TestCase):
    """
    Replicates a dialog of SIR (Semantic Information Retriever), by Bertram Rafael as described in
    - SIR: a computer program for semantic information retrieval - Bertram Rafael (1964)

    This system is interesting because it allows the user to teach the computer facts about concepts,
    then use these new concepts to answer questions.

    Relations in SIR include:
    - set-inclusion (dog is a mammal)
    - part-whole relationship (finger part of hand)
    - numeric quantity associated with the part-whole relationship (hand has 5 fingers)
    - set-membership (Fido is a dog)
    - left-to-right spatial relations
    - ownership

    It displays both the entity and the relation aspect of the same concept.

    Topics:
    - Teaching is-a relationships
    - Teaching concepts
    - Clarification messages stating missing knowledge

    """

    def test_sir(self):

        inferences = InferenceModule()

        facts = SIRModule(MemoryDbDataSource(MemoryDb()))

        tokenizer = BasicTokenizer()
        grammar = SimpleGrammarRulesParser().parse(get_grammar())
        grammar_module = GrammarModule(grammar)
        parser = BasicParser(grammar, tokenizer)
        sentence_context = SIRSentenceContext()

        model = Model([
            facts,
            inferences,
            grammar_module,
            sentence_context
        ])

        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        composer.sentence_context = sentence_context
        executor = AtomExecutor(composer, model)
        responder = SimpleResponder(model, executor)

        pipeline1 = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            TryFirst(composer),
            TryFirst(executor),
            TryFirst(responder)
        ])

        tests = [
            # both boy and person are new
            # inference: person :- boy
            # grammar rules: noun -> boy, noun -> person
            # relations: boy(id), person(id)
            ['Every boy is a person', 'I understand'],
            # both finger and hand are new
            # inference: part_of(finger, hand) / part_of(E1, E2) :- finger(E1), hand(E2)
            ['A finger is a part of a hand', 'I understand'],
            #     # ['Each person has two hands', 'The above sentence is ambiguous; please re-phrase it'],
            # # known concepts;
            ['There are two hands on each person', 'I understand'],
            # ['How many fingers does John have?', "Don't know whether finger is part of John"],
            # ['John is a boy', 'I understand'],
            # ['How many fingers does John have?', "How many finger per hand?"],
            # ['Every hand has 5 fingers', 'I understand'],
            # ['How many fingers does John have?', "The answer is 10"],
        ]

        logger = Logger()
        # logger.log_no_tests()
        logger.log_only_last_test()
        logger.log_products()

        tester = DialogTester(self, tests, pipeline1, logger)
        tester.run()

        print(logger)
