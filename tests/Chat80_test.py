import unittest
import pathlib

from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.module.InferenceModule import InferenceModule
from richard.store.MemoryDb import MemoryDb
from .chat80.Chat80Responder import Chat80Responder
from .chat80.Chat80Module import Chat80Module
from .chat80.chat80_grammar import get_grammar


class TestChat80(unittest.TestCase):
    """
    Mimics a Chat-80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)

    Topics:
    - long distance dependencies (extraposition)
    - proper nouns
    - superlatives ('largest')
    - relative clauses
    - aggregations
    - inference: in(A, B) -> contains(C, A), in(C, B).
    - different result formats: yes/no, scalar, list, table
    - query optimization: reordering and isolating sub-queries
    """

    def test_chat80(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/chat80/resources/"

        db = MemoryDb()
        db.import_csv('continent', path + "continent.csv")
        db.import_csv('ocean', path + "ocean.csv")
        db.import_csv('sea', path + "sea.csv")
        db.import_csv('river', path + "river.csv")
        db.import_csv('city', path + "city.csv")
        db.import_csv('country', path + "country.csv")
        db.import_csv('contains', path + "contains.csv")
        db.import_csv('borders', path + "borders.csv")

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")

        dialog_context = SimpleMemoryModule({
            "isa": Relation(attributes=["entity", "type"]),
        })
        sentence_context = SimpleMemoryModule({
            "format": Relation(attributes=["type", "variables", "units"]),
        })

        model = Model([
            Chat80Module(MemoryDbDataSource(db)),
            inferences,
            dialog_context,
            sentence_context
        ])

        tokenizer = BasicTokenizer()
        parser = BasicParser(get_grammar(), tokenizer)
        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        composer.sentence_context = sentence_context
        executor = AtomExecutor(composer, model)
        responder = SimpleResponder(model, executor, handler=Chat80Responder())

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
            ["How large is the smallest american country?", "0 ksqmiles"],
            ["What is the ocean that borders African countries?", "atlantic, indian_ocean"],
            ["What is the ocean that borders African countries and that borders Asian countries?", "indian_ocean"],
            ["What are the capitals of the countries bordering the Baltic?", [
                ['denmark', 'copenhagen'],
                ['east_germany', 'east_berlin'],
                ['finland', 'helsinki'],
                ['poland', 'warsaw'],
                ['soviet_union', 'moscow'],
                ['sweden', 'stockholm'],
                ['west_germany', 'bonn'],
            ]],
            ["Which countries are bordered by two seas?", "egypt, iran, israel, saudi_arabia, turkey"],
            ["How many countries does the Danube flow through?", 6],
            ["What are the countries south of the Equator and not in Australasia?", "angola, argentina, bolivia, botswana, brazil, burundi, chile, congo, ecuador, indonesia, lesotho, malagasy, malawi, mauritius, mozambique, paraguay, peru, rwanda, seychelles, south_africa, swaziland, tanzania, uruguay, zaire, zambia, zimbabwe"],
            ["What is the total area of countries south of the Equator and not in Australasia?", "10228 ksqmiles"],
            ["What is the average area of the countries in each continent?", [
                ["africa", "233 ksqmiles"],
                ["america", "496 ksqmiles"],
                ["asia", "485 ksqmiles"],
                ["australasia", "543 ksqmiles"],
                ["europe", "58 ksqmiles"]]],
            ["Is there more than one country in each continent?", 'no'],
            ["Is there some ocean that does not border any country?", "yes"],
            ["What are the countries from which a river flows into the Black_Sea?", "romania, soviet_union"],
            ["What are the continents no country in which contains more than two cities whose population exceeds 1 million?", "africa, antarctica, australasia"],
            ["Which country bordering the Mediterranean borders a country that is bordered by a country whose population exceeds the population of India?", "turkey"],
            ["Which countries have a population exceeding 10 million?", "afghanistan, algeria, argentina, australia, bangladesh, brazil, burma, canada, china, colombia, czechoslovakia, east_germany, egypt, ethiopia, france, india, indonesia, iran, italy, japan, kenya, mexico, morocco, nepal, netherlands, nigeria, north_korea, pakistan, peru, philippines, poland, south_africa, south_korea, soviet_union, spain, sri_lanka, sudan, taiwan, tanzania, thailand, turkey, united_kingdom, united_states, venezuela, vietnam, west_germany, yugoslavia, zaire"],
            ["Which countries with a population exceeding 10 million border the Atlantic?", "argentina, brazil, canada, colombia, france, mexico, morocco, netherlands, nigeria, south_africa, spain, united_kingdom, united_states, venezuela, west_germany, zaire"],
            ["What percentage of countries border each ocean?", [
                ['arctic_ocean', "2"],
                ['atlantic', "36"],
                ['indian_ocean', "14"],
                ['pacific', "20"],
                ['southern_ocean', "0"],
            ]],
            ["What countries are there in Europe?", "albania, andorra, austria, belgium, bulgaria, cyprus, czechoslovakia, denmark, east_germany, eire, finland, france, greece, hungary, iceland, italy, liechtenstein, luxembourg, malta, monaco, netherlands, norway, poland, portugal, romania, san_marino, spain, sweden, switzerland, united_kingdom, west_germany, yugoslavia"],
            ["Bye.", "Cheerio."],
        ]

        logger = Logger()
        logger.log_no_tests()
        # logger.log_all_tests()
        # logger.log_products()
        # logger.log_stats()

        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)

