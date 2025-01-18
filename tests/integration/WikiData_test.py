import pathlib
import unittest


from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from richard.data_source.WikidataDataSource import WikidataDataSource
from tests.integration.wikidata.write_grammar import get_write_grammar
from .wikidata.WikiDataSentenceContext import WikiDataSentenceContext
from .wikidata.WikidataModule import WikidataModule
from .wikidata.read_grammar import get_read_grammar


class TestWikiData(unittest.TestCase):
    """
    In this test we connect to Wikidata Query Service, using its SPARQL endpoint

    NB!    Results from Wikidata are cached to file, for speed and to avoid making too many requests

    Set result_cache_path to None to access Wikidata without the cache

    The endpoint is accessed via HTTP, so we need the requests library

    pip install requests

    """

    def test_wikidata(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/wikidata/resources/"
        result_cache_path = str(pathlib.Path(__file__).parent.resolve()) + "/wikidata/result_cache/"

        # map domain predicates to one or more Wikidata predicates
        inferences = InferenceModule()
        inferences.import_rules(path + "mapping.pl")
        inferences.import_rules(path + "sentences.pl")

        sentence_context = WikiDataSentenceContext()
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
        composer.sentence_context = sentence_context
        executor = AtomExecutor(composer, model)

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_write_grammar())
        generator = BasicGenerator(write_grammar, model)

        pipeline = Pipeline([
            FindOne(parser),
            TryFirst(composer),
            TryFirst(executor),
        ], generator=generator)

        tests = [
            ["Where was madonna born?", "Bay City"],
        ]

        logger = Logger()
        # logger.log_no_tests()
        logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)

