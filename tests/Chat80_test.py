from math import ceil
import unittest
import pathlib
import cProfile
import time

from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.Solver import Solver
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.store.MemoryDb import MemoryDb
from .chat80.Chat80Responder import Chat80Responder
from .chat80.Chat80Module import Chat80Module
from .chat80.chat80_grammar import get_grammar


class TestChat80(unittest.TestCase):
    """
    Mimics a Chat80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    Topics:
    - proper nouns
    - superlatives ('largest')
    - relative clauses
    - aggregations
    - inference: in(A, B) -> contains(A, C) in(C, B).
    - query optimization
    - different result formats: yes/no, scalar, list, table
    """
   
    def test_chat80(self):
        # cProfile.runctx('self.do()', globals(), locals(), None, 'cumulative')
        self.do()

    def do(self):

        db = MemoryDb()
        path = str(pathlib.Path(__file__).parent.resolve()) + "/chat80/resources/"

        db.import_csv('continent', path + "continent.csv")
        db.import_csv('ocean', path + "ocean.csv")
        db.import_csv('sea', path + "sea.csv")
        db.import_csv('river', path + "river.csv")
        db.import_csv('city', path + "city.csv")
        db.import_csv('country', path + "country.csv")
        db.import_csv('contains', path + "contains.csv")
        db.import_csv('borders', path + "borders.csv")

        data_source = MemoryDbDataSource(db)
        model = Model([Chat80Module(data_source)])
        solver = Solver(model)
        grammar = get_grammar()

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser, model)
        executor = AtomExecutor(composer, solver)
        responder = SimpleResponder(composer, executor, handler=Chat80Responder())

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor),
            FindOne(responder)
        ])

        tests = [
            ["What rivers are there?", "amazon, amu_darya, amur, brahmaputra, colorado, congo_river, cubango, danube, don, elbe, euphrates, ganges, hwang_ho, indus, irrawaddy, lena, limpopo, mackenzie, mekong, mississippi, murray, niger_river, nile, ob, oder, orange, orinoco, parana, rhine, rhone, rio_grande, salween, senegal_river, tagus, vistula, volga, volta, yangtze, yenisei, yukon, zambesi"],
            ["Does Afghanistan border China?", "yes"],
            ["What is the capital of Upper_Volta?", "ouagadougou"],
            ["Where is the largest country?", "northern_asia"],
            ["Which countries are European?", "albania, andorra, austria, belgium, bulgaria, cyprus, czechoslovakia, denmark, east_germany, eire, finland, france, greece, hungary, iceland, italy, liechtenstein, luxembourg, malta, monaco, netherlands, norway, poland, portugal, romania, san_marino, spain, sweden, switzerland, united_kingdom, west_germany, yugoslavia"],
            ["Which country's capital is London?", "united_kingdom"],
            ["Which is the largest african country?", "sudan"],
            ["How large is the smallest american country?", 0],
            ["What is the ocean that borders African countries?", "atlantic, indian_ocean"],
            ["What is the ocean that borders African countries and that borders Asian countries?", "indian_ocean"],
            ["What are the capitals of the countries bordering the Baltic?", [
                ['denmark', 'copenhagen'], 
                ['east_germany', 'east_berlin'], 
                ['finland', 'helsinki'], 
                ['poland', 'warsaw'], 
                ['soviet_union', 'moscow'], 
                ['sweden', 'stockholm'], 
                ['west_germany', 'bonn']
            ]],
            ["Which countries are bordered by two seas?", "egypt, iran, israel, saudi_arabia, turkey"],
            ["How many countries does the Danube flow through?", 6],
            ["What are the countries south of the Equator and not in Australasia?", "angola, argentina, bolivia, botswana, brazil, burundi, chile, congo, ecuador, indonesia, lesotho, malagasy, malawi, mauritius, mozambique, paraguay, peru, rwanda, seychelles, south_africa, swaziland, tanzania, uruguay, zaire, zambia, zimbabwe"],
            ["What is the total area of countries south of the Equator and not in Australasia?", 10228],
            ["What is the average area of the countries in each continent?", [
                ["africa", 233.58333333333334],
                ["america", 496.3225806451613],
                ["asia", 485.2307692307692],
                ["australasia", 543.5],
                ["europe", 58.3125]]],
            ["Is there more than one country in each continent?", 'no'],
            ["Is there some ocean that does not border any country?", "yes"],
            ["What are the countries from which a river flows into the Black_Sea?", "austria, czechoslovakia, hungary, romania, soviet_union, west_germany, yugoslavia"],
            ["What are the continents no country in which contains more than two cities whose population exceeds 1 million?", "africa, antarctica, australasia"],
            # ["Which country bordering the Mediterranean borders a country that is bordered by a country whose population exceeds the population of India?", "turkey"],
            ["Which countries have a population exceeding 10 million?", "afghanistan, algeria, argentina, australia, bangladesh, brazil, burma, canada, china, colombia, czechoslovakia, east_germany, egypt, ethiopia, france, india, indonesia, iran, italy, japan, kenya, mexico, morocco, nepal, netherlands, nigeria, north_korea, pakistan, peru, philippines, poland, south_africa, south_korea, soviet_union, spain, sri_lanka, sudan, taiwan, tanzania, thailand, turkey, united_kingdom, united_states, venezuela, vietnam, west_germany, yugoslavia, zaire"],
            ["Which countries with a population exceeding 10 million border the Atlantic?", "argentina, brazil, canada, colombia, france, mexico, morocco, netherlands, nigeria, south_africa, spain, united_kingdom, united_states, venezuela, west_germany, zaire"],
            ["What percentage of countries border each ocean?", [
                ['arctic_ocean', 2.564102564102564],
                ['atlantic', 36.53846153846153],
                ['indian_ocean', 14.102564102564102],
                ['pacific', 20.51282051282051],
                ['southern_ocean', 0.0],
            ]],
            ["What countries are there in Europe?", "albania, andorra, austria, belgium, bulgaria, cyprus, czechoslovakia, denmark, east_germany, eire, finland, france, greece, hungary, iceland, italy, liechtenstein, luxembourg, malta, monaco, netherlands, norway, poland, portugal, romania, san_marino, spain, sweden, switzerland, united_kingdom, west_germany, yugoslavia"],
            ["Bye.", "Cheerio."]
        ]

        for test in tests:
            question, answer = test
            print()
            print(question)
            start_time = time.perf_counter()
            request = SentenceRequest(question)
            try:
                result = pipeline.enter(request)
            except:
                print(parser.get_tree(request))
                print(composer.format_semantics(request))
                print(composer.format_optimized_semantics(request))
                print(executor.get_results(request))
                print(responder.get_response(request))
            
            end_time = time.perf_counter()
            print(str(ceil((end_time - start_time) * 1000)) + " msecs")

            if not result.error_code == "":
                print(result.error_code, result.error_args) 
                break

            results = responder.get_response(request)
            print(results)
            print(composer.format_optimized_semantics(request))
            if results != answer:
                print(parser.get_tree(request))
                print(composer.format_semantics(request))
                print(composer.format_optimized_semantics(request))
                print(executor.get_results(request))
                print(responder.get_response(request))
            self.assertEqual(answer, results)
            
