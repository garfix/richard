import pathlib
import unittest


from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.entity.Relation import Relation
from richard.module.InferenceModule import InferenceModule
from richard.module.SimpleMemoryModule import SimpleMemoryModule
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from tests.wikidata.WikidataModule import WikidataModule
from tests.wikidata.WikidataResponder import WikidataResponder
from .wikidata.grammar import get_grammar

from richard.data_source.WikidataDataSource import WikidataDataSource


class TestWikiData(unittest.TestCase):
    """
    In this test we connect to Wikidata Query Service, using its SPARQL endpoint

    pip install requests

    """

    def test_wikidata(self):


        path = str(pathlib.Path(__file__).parent.resolve()) + "/wikidata/resources/"

        # skip for now
        # return

        inferences = InferenceModule()
        inferences.import_rules(path + "mapping.pl")

        # dialog_context = SimpleMemoryModule({
        #     "isa": Relation(attributes=["entity", "type"]),
        # })
        sentence_context = SimpleMemoryModule({
            "format": Relation(attributes=["type", "variables"]),
        })

        model = Model([
            inferences,
            # dialog_context,
            sentence_context,
            WikidataModule(WikidataDataSource()),
        ])

        tokenizer = BasicTokenizer()
        parser = BasicParser(get_grammar(), tokenizer)
        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        executor = AtomExecutor(composer, model)
        responder = SimpleResponder(model, executor, handler=WikidataResponder())

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor),
            FindOne(responder)
        ])


        # first goal:

        tests = [
            ["Where was Madonna born?", "Bay City"],
        ]

        logger = Logger()
        # logger.log_no_tests()
        # logger.log_all_tests()
        logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)

