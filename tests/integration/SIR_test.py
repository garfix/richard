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

    It displays both the entity and the relation aspect of the same concept.

    Topics:
    - Teaching is-a relationships
    - Teaching concepts
    - Clarification messages stating missing knowledge

    """

    def test_sir(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/sir/resources/"

        # create a database

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE isa (entity TEXT, type TEXT)")
        cursor.execute("CREATE TABLE part_of (part TEXT, whole TEXT)")
        cursor.execute("CREATE TABLE part_of_n (part TEXT, whole TEXT, number INTEGER)")

        data_source = Sqlite3DataSource(connection)
        facts = SIRModule(data_source)

        # define some inference rules

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")

        # sentence scoped facts

        sentence_context = BasicSentenceContext()

        # define the pipeline

        grammar = SimpleGrammarRulesParser().parse(get_grammar())
        parser = BasicParser(grammar)

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
            # number
            ['Every boy is a person', 'I understand'],
            ['A finger is a part of a hand', 'I understand'],
            ['There are two hands on each person', 'I understand'],
            ['How many fingers does John have?', "Don't know whether finger is part of John"],
            ['John is a boy', 'I understand'],
            ['How many fingers does John have?', "How many finger per hand?"],
            ['Every hand has 5 fingers', 'I understand'],
            ['How many fingers does John have?', "The answer is 10"],

            # set-inclusion
            ['Every keypunch-operator is a girl', 'I understand'],
            ['Any girl is an example of a person', 'I understand'],
            ['Is a keypunch-operator a person?', 'Yes'],
            ['Is a person a person?', 'Yes'],
            ['Is a person a girl?', 'Sometimes'],
            ['Is a monkey a keypunch-operator?', 'Insufficient information'],
        ]

        logger = Logger()
        logger.log_no_tests()
        logger.log_only_last_test()
        logger.log_all_tests()
        logger.log_products()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)
