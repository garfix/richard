import pathlib
import sqlite3
import unittest

from richard.block.TryFirst import TryFirst
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.processor.parser.BasicParser import BasicParser
from tests.integration.sir.SIRModule import SIRModule
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

        path = str(pathlib.Path(__file__).parent.resolve()) + "/sir/resources/"

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE isa (entity TEXT, type TEXT)")
        cursor.execute("CREATE TABLE part_of (part TEXT, whole TEXT)")
        cursor.execute("CREATE TABLE part_of_n (part TEXT, whole TEXT, number INTEGER)")

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")

        data_source = Sqlite3DataSource(connection)
        facts = SIRModule(data_source)

        grammar = SimpleGrammarRulesParser().parse(get_grammar())
        parser = BasicParser(grammar)
        sentence_context = BasicSentenceContext()

        model = Model([
            facts,
            inferences,
            sentence_context
        ])

        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        composer.sentence_context = sentence_context
        executor = AtomExecutor(composer, model)
        responder = SimpleResponder(model, executor)

        pipeline = Pipeline([
            TryFirst(parser),
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
            ['How many fingers does John have?', "Don't know whether finger is part of John"],
            ['John is a boy', 'I understand'],
            ['How many fingers does John have?', "How many finger per hand?"],
            ['Every hand has 5 fingers', 'I understand'],
            ['How many fingers does John have?', "The answer is 10"],
        ]

        logger = Logger()
        logger.log_no_tests()
        # logger.log_only_last_test()
        # logger.log_all_tests()
        # logger.log_products()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)
