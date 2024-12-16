import pathlib
import unittest


from richard.block.TryFirst import TryFirst
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from richard.data_source.WikidataDataSource import WikidataDataSource
from .wikidata.WikidataModule import WikidataModule
from .wikidata.grammar import get_grammar


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

        sentence_context = BasicSentenceContext()
        wikidata = WikidataModule(WikidataDataSource(result_cache_path=result_cache_path))

        model = Model([
            inferences,
            sentence_context,
            wikidata,
        ])

        grammar = SimpleGrammarRulesParser().parse(get_grammar())
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        composer.sentence_context = sentence_context
        executor = AtomExecutor(composer, model)
        responder = SimpleResponder(model, executor)

        pipeline = Pipeline([
            FindOne(parser),
            TryFirst(composer),
            TryFirst(executor),
            TryFirst(responder)
        ])

        tests = [
            ["Where was madonna born?", "Bay City"],
        ]

        logger = Logger()
        logger.log_no_tests()
        # logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)

