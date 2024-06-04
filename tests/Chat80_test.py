import unittest

from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.Instance import Instance
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from .chat80.chat80_model import model
from .chat80.chat80_grammar import get_grammar

class TestChat80(unittest.TestCase):
    """
    Mimics a Chat80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    Topics:
    - attributes ('capital of')
    - superlatives ('largest')
    - relative clauses
    - aggregations
    """
   
    def test_chat80(self):

        tokenizer = BasicTokenizer()
        parser = BasicParser(get_grammar(model), tokenizer)
        composer = SemanticComposer(parser)
        executor = SemanticExecutor(composer)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor)
        ])

        tests = [
            ["What rivers are there?", set([Instance(entity='river', id='amazon'), Instance(entity='river', id='brahmaputra'), Instance(entity='river', id='danube')])],
            ["Does Afghanistan border China?", set([Instance(entity='country', id='afghanistan')])],
            ["What is the capital of Upper_Volta?", set([Instance(entity='city', id='ouagadougou')])],
            ["Where is the largest country?", set([Instance(entity='place', id='northern_asia')])],
            ["Which countries are European?", set([Instance(entity='country', id='united_kingdom'), Instance(entity='country', id='albania'), Instance(entity='country', id='poland'), Instance(entity='country', id='hungary'), Instance(entity='country', id='czechoslovakia')])],
            ["Which country's capital is London?", set([Instance(entity='country', id='united_kingdom')])],
            ["Which is the largest african country?", set([Instance(entity='country', id='mozambique')])],
            ["How large is the smallest american country?", set([157.47])],
            ["What is the ocean that borders African countries?", set([Instance(entity='ocean', id='atlantic'), Instance(entity='ocean', id='indian_ocean')])],
            ["What is the ocean that borders African countries and that borders Asian countries?", set([Instance(entity='ocean', id='indian_ocean')])],
            ["What are the capitals of the countries bordering the Baltic?", [[Instance(entity='country', id='poland'), 'warsaw']]],
            ["Which countries are bordered by two seas?", set([Instance(entity='country', id='soviet_union')])],
            ["How many countries does the Danube flow through?", 2],
            ["What are the countries south of the Equator and not in Australasia?", set([Instance(entity='country', id='congo'), Instance(entity='country', id='mozambique'), Instance(entity='country', id='paraguay'), Instance(entity='country', id='rwanda')])],
            ["What is the total area of countries south of the Equator and not in Australasia?", 603.472],
            # ["What is the average area of the countries in each continent?", []]
        ]

        for test in tests:
            question, answer = test
            print(question)
            request = SentenceRequest(question)
            result = pipeline.enter(request)

            if not result.error_code == "":
                print(result.error_code, result.error_args) 
                break

            results = executor.get_results(request)
            self.assertEqual(answer, results)
            
