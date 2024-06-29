import unittest

from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.Solver import Solver
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.type.OrderedSet import OrderedSet
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Instance import Instance
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from tests.chat80_2.Chat80Module import Chat80Module
from .chat80_2.chat80_grammar import get_grammar
from .chat80_2.chat80_db import db

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

        data_source = MemoryDbDataSource(db)
        model = Model([Chat80Module(data_source)])
        solver = Solver(model)
        grammar = get_grammar(model)

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, solver)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor)
        ])

        tests = [
            ["What rivers are there?", [{'S1': Instance(entity='river', id='amazon')}, {'S1': Instance(entity='river', id='brahmaputra')}, {'S1': Instance(entity='river', id='danube')}, {'S1': Instance(entity='river', id='don')}, {'S1': Instance(entity='river', id='volga')}]],
            ["Does Afghanistan border China?", [{'S1': Instance(entity='country', id='afghanistan')}]],
            # ["What is the capital of Upper_Volta?", OrderedSet([Instance(entity='city', id='ouagadougou')])],
            # ["Where is the largest country?", OrderedSet([Instance(entity='place', id='northern_asia')])],
            # ["Which countries are European?", OrderedSet([Instance(entity='country', id='united_kingdom'), Instance(entity='country', id='albania'), Instance(entity='country', id='poland'), Instance(entity='country', id='hungary'), Instance(entity='country', id='czechoslovakia'), Instance(entity='country', id='romania'), Instance(entity='country', id='yugoslavia'), Instance(entity='country', id='austria'), Instance(entity='country', id='west_germany')])],
            # ["Which country's capital is London?", OrderedSet([Instance(entity='country', id='united_kingdom')])],
            # ["Which is the largest african country?", OrderedSet([Instance(entity='country', id='mozambique')])],
            # ["How large is the smallest american country?", OrderedSet([157.47])],
            # ["What is the ocean that borders African countries?", OrderedSet([Instance(entity='ocean', id='atlantic'), Instance(entity='ocean', id='indian_ocean')])],
            # ["What is the ocean that borders African countries and that borders Asian countries?", OrderedSet([Instance(entity='ocean', id='indian_ocean')])],
            # ["What are the capitals of the countries bordering the Baltic?", [[Instance(entity='country', id='poland'), 'warsaw']]],
            # ["Which countries are bordered by two seas?", OrderedSet([Instance(entity='country', id='soviet_union')])],
            # ["How many countries does the Danube flow through?", 2],
            # ["What are the countries south of the Equator and not in Australasia?", OrderedSet([Instance(entity='country', id='congo'), Instance(entity='country', id='mozambique'), Instance(entity='country', id='paraguay'), Instance(entity='country', id='rwanda')])],
            # ["What is the total area of countries south of the Equator and not in Australasia?", 603.472],
            # ["What is the average area of the countries in each continent?", [
            #     [Instance(entity='continent', id='africa'), 105.869],
            #     [Instance(entity='continent', id='america'), 3615.122],
            #     [Instance(entity='continent', id='asia'), 1973.1815],
            #     [Instance(entity='continent', id='australasia'), 2967.909],
            #     [Instance(entity='continent', id='europe'), 75.73519999999999]]],
            # ["Is there more than one country in each continent?", False],
            # ["Is there some ocean that does not border any country?", OrderedSet([Instance(entity='ocean', id='southern_ocean'), Instance(entity='ocean', id='arctic_ocean')])],
            # ["What are the countries from which a river flows into the Black_Sea?", OrderedSet([Instance(entity='country', id='soviet_union'), Instance(entity='country', id='hungary'), Instance(entity='country', id='czechoslovakia'), Instance(entity='country', id='romania'), Instance(entity='country', id='yugoslavia'), Instance(entity='country', id='austria'), Instance(entity='country', id='west_germany')])]
        ]

        for test in tests:
            question, answer = test
            print()
            print(question)
            request = SentenceRequest(question)
            result = pipeline.enter(request)

            if not result.error_code == "":
                print(result.error_code, result.error_args) 
                break

            results = executor.get_results(request)
            print(results)
            if results != answer:
                print(parser.get_tree(request))
                print(composer.format_tuples(request))
            self.assertEqual(answer, results)
            
