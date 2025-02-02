import pathlib
import unittest


from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.grammar.en_us_write import get_en_us_write_grammar
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from richard.data_source.WikidataDataSource import WikidataDataSource
from tests.integration.wikidata.write_grammar import get_write_grammar
from .WikidataSentenceContext import WikidataSentenceContext
from .WikidataModule import WikidataModule
from .read_grammar import get_read_grammar


class TestWikiData(unittest.TestCase):
    """
    In this test we connect to Wikidata Query Service, using its SPARQL endpoint

    NB!    Results from Wikidata are cached to file, for speed and to avoid making too many requests

    Set result_cache_path to None to access Wikidata without the cache

    The endpoint is accessed via HTTP, so we need the requests library

    pip install requests

    """

    def test_wikidata(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/resources/"
        result_cache_path = str(pathlib.Path(__file__).parent.resolve()) + "/result_cache/"

        # map domain predicates to one or more Wikidata predicates
        inferences = InferenceModule()
        inferences.import_rules(path + "mapping.pl")
        inferences.import_rules(path + "sentences.pl")

        sentence_context = WikidataSentenceContext()
        wikidata = WikidataModule(WikidataDataSource(result_cache_path=result_cache_path))

        model = Model([
            inferences,
            sentence_context,
            wikidata,
        ])

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar())
        parser = BasicParser(read_grammar)
        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        executor = AtomExecutor(composer, model)

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_en_us_write_grammar() + get_write_grammar())
        generator = BasicGenerator(write_grammar, model, sentence_context)

        system = System(
            model=model,
            input_pipeline=[
                FindOne(parser),
                TryFirst(composer),
                TryFirst(executor),
            ],
            output_generator=generator)

        tests = [
            ["Where was madonna born?", "Bay City"],
        ]

        logger = Logger()
        logger.log_no_tests()
        # logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests, system, logger)
        tester.run()

        print(logger)

