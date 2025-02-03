import unittest
import pathlib

from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.entity.SentenceRequest import SentenceRequest
from richard.grammar.en_us_write import get_en_us_write_grammar
from richard.module.BasicDialogContext import BasicDialogContext
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from richard.module.InferenceModule import InferenceModule
from .HelloWorldDB import HellowWorldDB
from .HelloWorldModule import HelloWorldModule
from .read_grammar import get_read_grammar
from .write_grammar import get_write_grammar


class TestHelloWorld(unittest.TestCase):
    """
    A basic application that creates a test and shows how to interact with the system.
    """

    def test_hello_world(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        # define the database

        db = HellowWorldDB()
        facts = HelloWorldModule(db)

        # define the intents and other inferences

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")
        inferences.import_rules(path + "intents.pl")

        # define the data sources that have sentence and dialog scope, respectively

        sentence_context = BasicSentenceContext()
        dialog_context = BasicDialogContext()

        # define the model

        model = Model([
            facts,
            inferences,
            sentence_context,
            dialog_context
        ])

        # define the pipeline

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar())
        parser = BasicParser(read_grammar)

        composer = SemanticComposer(parser, query_optimizer = BasicQueryOptimizer(model))
        executor = AtomExecutor(composer, model)

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_en_us_write_grammar() + get_write_grammar())
        generator = BasicGenerator(write_grammar, model, sentence_context)

        # define the system

        system = System(
            model=model,
            input_pipeline=[
                FindOne(parser),
                TryFirst(composer),
                TryFirst(executor)
            ],
            output_generator=generator
        )

        # test the system

        tests = [
            ["Hello world", "Hi there!"],
            ["What rivers are there?", "amazon, amu_darya, amur, brahmaputra, colorado, congo_river, cubango, danube, don, elbe, euphrates, ganges, hwang_ho, indus, irrawaddy, lena, limpopo, mackenzie, mekong, mississippi, murray, niger_river, nile, ob, oder, orange, orinoco, parana, rhine, rhone, rio_grande, salween, senegal_river, tagus, vistula, volga, volta, yangtze, yenisei, yukon, zambesi"],
        ]

        # comment in the following rules to see intermediate results

        logger = Logger()
        logger.log_no_tests()
        # logger.log_all_tests()
        # logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests, system, logger)
        tester.run()

        print(logger)

        # how to actually use the system

        system.enter(SentenceRequest("Hello world"))
        output = system.read_output()
        # print(output)
