import pathlib
import unittest

from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.grammar.en_us_write import get_en_us_write_grammar
from richard.module.BasicOutputBuffer import BasicOutputBuffer
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from .CooperDB import CooperDB
from .CooperModule import CooperModule
from .write_grammar import get_write_grammar
from .read_grammar1 import get_read_grammar1
from .read_grammar2 import get_read_grammar2


class TestCooper(unittest.TestCase):
    """
    Replicates a dialog of William S. Cooper's system as described in
    - Fact Retrieval and Deductive Question-Answering Informatlon Retrieval Systems - Cooper (1964)

    Topics:
    - Sentences that can either be statements or yes/no questions ("magnesium is a metal")
    - Aristotelian logic
    - Learning names and concepts
    - Learning rules
    - Users with different roles
    - Adverbs ("rapidly")
    - the name "magnesium oxide" implies that it is an oxide

    Cooper's (unnamed) system has a knowledge base that contains information like "ferrous sulfide is a dark-gray compound that is brittle".
    This information is entered as natural language and stored in logical form by a system-user with write-access.
    A user with only read-access can query the system thus: "ferrous sulfide is dark gray". And the system responds with "True" or "False".
    The system deduces this fact from the available knowledge using Aristotelian logic, which uses these sentences
    - All x's are y's
    - No x's are y's
    - Some x's are y's
    - Not all x's are y's
    """

    def test_cooper(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        # create a database

        data_source = CooperDB()
        facts = CooperModule(data_source)

        # define inference rules

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")

        # a data source to store information for output

        output_buffer = BasicOutputBuffer()

        # define the model

        model = Model([
            facts,
            inferences,
            output_buffer,
        ])

        # define the first pipeline

        grammar1 = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar1())
        parser = BasicParser(grammar1)

        composer = SemanticComposer(parser, query_optimizer = BasicQueryOptimizer(model))
        executor = AtomExecutor(composer, model)

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_en_us_write_grammar() + get_write_grammar())
        generator = BasicGenerator(write_grammar, model, output_buffer)

        # define the first system

        system1 = System(
            model=model,
            input_pipeline=[
                FindOne(parser),
                TryFirst(composer),
                TryFirst(executor),
            ],
            output_generator=generator
        )

        # define the second pipeline

        grammar2 = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar2())
        parser = BasicParser(grammar2)

        composer = SemanticComposer(parser, query_optimizer = BasicQueryOptimizer(model))
        executor = AtomExecutor(composer, model)

        # define the second system

        system2 = System(
            model=model,
            input_pipeline=[
                FindOne(parser),
                TryFirst(composer),
                TryFirst(executor),
            ],
            output_generator=generator
        )

        tests1 = [
            ["magnesium is a metal", "OK"],
            ["magnesium burns rapidly", "OK"],
            ["magnesium oxide is a white metallic oxide", "OK"],
            ['oxygen is a nonmetal', 'OK'],
            ['ferrous sulfide is a dark-gray compound that is brittle', 'OK'],
            ['iron is a metal', 'OK'],
            ['sulfur is a nonmetal', 'OK'],
            ['gasoline is a fuel', 'OK'],
            ['gasoline is combustable', 'OK'],
            ['combustable things burn', 'OK'],
            ['fuels are combustable', 'OK'],
            ['ice is a solid', 'OK'],
            ['steam is a gas', 'OK'],
            ['magnesium is an element', 'OK'],
            ['iron is an element', 'OK'],
            ['sulfur is an element', 'OK'],
            ['oxygen is an element', 'OK'],
            ['nitrogen is an element', 'OK'],
            ['hydrogen is an element', 'OK'],
            ['carbon is an element', 'OK'],
            ['copper is an element', 'OK'],
            ['salt is a compound', 'OK'],
            ['sugar is a compound', 'OK'],
            ['water is a compound', 'OK'],
            ['sulfuric acid is a compound', 'OK'],
            ['elements are not compounds', 'OK'],
            ['salt is sodium chloride', 'OK'],
            ['sodium chloride is salt', 'OK'],
            ['oxides are compounds', 'OK'],
            ['metals are metallic', 'OK'],
            ['no metal is a nonmetal', 'OK'],
            ['dark-gray things are not white', 'OK'],
            ['a solid is not a gas', 'OK'],
            ['any thing that burns rapidly burns', 'OK'],
        ]

        tests2 = [
            ["magnesium is a metal", "True"],
            ["magnesium is not a metal", "False"],
            ["magnesium is a nonmetal", "False"],
            ["magnesium is not a nonmetal", "True"],
            ["magnesium is a metal that burns rapidly", "True"],
            ["magnesium is magnesium", "True"],
            ["some oxides are white", "True"],
            ["no oxide is white", "False"],
            ["oxides are not white", "False"],
            ["magnesium oxide is an oxide", "True"],
            ["every oxide is an oxide", "True"],
            ["ferrous sulfide is dark-gray", "True"],
            ["ferrous sulfide is a brittle compound", "True"],
            ["ferrous sulfide is not brittle", "False"],
            ["some sulfides are brittle", "True"],
            ["ferrous sulfide is not a compound that is not dark-gray", "True"],
            ["anything that is not a compound is not ferrous sulfide", "True"],
            ["no dark-gray thing is a sulfide", "False"],
            ["ferrous sulfide is white", "False"],
            ["sodium chloride is a compound", "True"],
            ["salt is an element", "False"],
            ["sodium chloride is an element", "False"],
            ["gasoline is a fuel that burns", "True"],
        ]

        logger = Logger()
        logger.log_no_tests()
        # logger.log_all_tests()
        # logger.log_only_last_test()
        # logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests1, system1, logger)
        tester.run()

        # print(logger)

        tester = DialogTester(self, tests2, system2, logger)
        tester.run()

        print(logger)
