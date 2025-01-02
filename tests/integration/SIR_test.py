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
        cursor.execute("CREATE TABLE identical (entity1 TEXT, entity2 TEXT)")
        cursor.execute("CREATE TABLE part_of (part TEXT, whole TEXT)")
        cursor.execute("CREATE TABLE part_of_n (part TEXT, whole TEXT, number INTEGER)")
        cursor.execute("CREATE TABLE own (person TEXT, thing TEXT)")
        cursor.execute("CREATE TABLE just_left_of (thing1 TEXT, thing2 TEXT)")
        cursor.execute("CREATE TABLE left_of (thing1 TEXT, thing2 TEXT)")

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
            # set-inclusion
            ['Every keypunch-operator is a girl', 'I understand'],
            ['Any girl is an example of a person', 'I understand'],
            ['Is a keypunch-operator a person?', 'Yes'],
            ['Is a person a person?', 'Yes'],
            ['Is a person a girl?', 'Sometimes'],
            ['Is a monkey a keypunch-operator?', 'Insufficient information'],

            # set-membership
            ['Max is an IBM-7094', 'I understand'],
            ['An IBM-7094 is a computer', 'I understand'],
            ['Is Max a computer?', 'Yes'],
            # the rest of the section is semantically questionable (missing referent)
            # ['The boy is an MIT-student', 'I understand'], # G02840 is a boy
            # ['Every MIT-student is a bright-person', 'I understand'],
            # ['Is the boy a bright-person', 'Yes'],
            # ['John is a boy', 'I understand'],
            # ['Is the boy a bright-person', 'Which boy?'], # G02840 John

            # equivalence
            # commented out sentences are semantically questionable (missing referent)
            # ['The man is a jerk', 'I understand'], # G02840 is the man
            ['Jack is a dope', 'I understand'],
            ['John is Jack', 'I understand'],
            ['Is John a dope?', 'Yes'],
            # ['Is the man a dope?', 'Insufficient information'],
            # ['John is the man', 'I understand'],
            # ['Is the man a dope?', 'Yes'],
            # ['Jim is a man', 'I understand'],
            # ['Is the man a dope?', 'Which man?'], # G02840 Jim

            # ownership, general
            ['Every fireman owns a pair-of-red-suspenders', 'I understand'],
            ['Does a pair-of-red-suspenders own a pair-of-red-suspenders?', 'No, they are the same'],
            ['Does a doctor own a pair-of-red-suspenders?', 'Insufficient information'],
            ['A firechief is a fireman', 'I understand'],
            ['Does a firechief own a pair-of-red-suspenders?', 'Yes'],

            # ownership, specific
            ['Alfred owns a log-log-decitrig', 'I understand'],
            ['A log-log-decitrig is a slide-rule', 'I understand'],
            ['Does Alfred own a slide-rule?', 'Yes'],
            ['Every engineering-student owns a slide-rule', 'I understand'],
            ['Vernon is a tech-man', 'I understand'],
            ['A tech-man is an engineering-student', 'I understand'],
            ['Does Vernon own a slide-rule?', 'Yes'],
            ['Does an engineering-student own a log-log-decitrig?', 'Insufficient information'],
            ['Alfred is a tech-man', 'I understand'],
            ['Does an engineering-student own a log-log-decitrig?', 'Yes'],

            # part-whole, general
            ['A nose is part of a person', 'I understand'],
            ['A nostril is part of a nose', 'I understand'],
            ['A professor is a teacher', 'I understand'],
            ['A teacher is a person', 'I understand'],
            ['Is a nostril part of a professor?', 'Yes'],
            ['Is a nose part of a nose?', 'No, part means proper subpart'],
            ['A person is a living-creature', 'I understand'],
            ['Is a nostril part of a living-creature?', 'Sometimes'],
            ['Is a living-creature part of a nose?', 'No, but the reverse is sometimes true'], # No, nose is sometimes part of living-creature

            # part-whole, specific
            ['A van-dyke is part of Ferren', 'I understand'],
            ['A van-dyke is a beard', 'I understand'],
            ['Is a beard part of Ferren?', 'Yes'],
            ['A crt is a display-device', 'I understand'],
            ['A crt is part of the PDP-1', 'I understand'],
            ['Sam is the PDP-1', 'I understand'],
            ['A screen is part of every display-device', 'I understand'],
            ['Is a screen part of Sam?', 'Yes'],
            ['A beard is part of a beatnik', 'I understand'],
            ['Every coffee-house-customer is a beatnik', 'I understand'],
            ['Buzz is a coffee-house-customer', 'I understand'],
            ['Is a beard part of Buzz?', 'Yes'],

            # number
            ['Every boy is a person', 'I understand'],
            ['A finger is a part of a hand', 'I understand'],
            ['There are two hands on each person', 'I understand'],
            ['How many fingers does John have?', "Don't know whether finger is part of John"],
            ['John is a boy', 'I understand'],
            ['How many fingers does John have?', "How many finger per hand?"],
            ['Every hand has 5 fingers', 'I understand'],
            ['How many fingers does John have?', "The answer is 10"],

            # left-to-right position
            # book-telephone-pad
            ['The telephone is just to the right of the book', 'I understand'],
            ['The telephone is just to the left of the pad', 'I understand'],
            ['Is the pad just to the right of the book?', 'No'],
            ['Is the book to the left of the pad?', 'Yes'],
            ['The pad is to the right of the telephone', 'I understand'],
            ['The pad is to the left of the telephone', 'The above statement is impossible'],
            # ['The ash-tray is to the left of the book', 'I understand'],
            # ['The pencil is to the left of the pad', 'I understand'],
            # ['The paper is to the right of the book', 'I understand'],
            # ['Where is the pad?', 'Just to the right of the telephone'], # Somewhere to the right of the following .. (pencil)
            # ['What is the position of the pad?', 'The left-to-right order is as follows: ash-tray (book telephone pad) paper)'], # To further specify the positionsyou must indicate wherethe pencil iswith respect to the ash-tray
            # ['The book is just to the right of the ash-tray', 'I understand'],
            # ['What is the position of the pad?', 'The left-to-right order is as follows: pencil (ash-tray book telephone pad) paper)'],
            # ['A telephone is an audio-transducer', 'I understand'],
            # ['A diafragm is part of an audio-transducer', 'I understand'],
            # ['Where is a diafragm?', 'Just to the left of the pad. Justto the right of the book.'], # Somewhere to the left of the following... (paper)
        ]

        logger = Logger()
        logger.log_no_tests()
        logger.log_only_last_test()
        # logger.log_all_tests()
        logger.log_products()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)
