import unittest
import pathlib

from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.grammar.en_us_write import get_en_us_write_grammar
from richard.module.BasicDialogContext import BasicDialogContext
from richard.module.BasicOutputBuffer import BasicOutputBuffer
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_composer.optimizer.BasicQueryOptimizer import BasicQueryOptimizer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.processor.parser.BasicParser import BasicParser
from richard.module.InferenceModule import InferenceModule
from .Chat80DB import Chat80DB
from .write_grammar import get_write_grammar
from .Chat80Module import Chat80Module
from .read_grammar import get_read_grammar


class TestChat80(unittest.TestCase):
    """
    Replicates a Chat-80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    CHAT-80 is mainly described in
    - Efficient Processing of Interactive Relational Database Queries Expressed in Logic - Warren (1981)
    - An efficient easily adaptable system for interpreting natural language queries - Pereira, Warren (1982)

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

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        # define the database

        db = Chat80DB()
        facts = Chat80Module(db)

        # define the intents and other inferences

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")
        inferences.import_rules(path + "intents.pl")

        # a data source to store information for output

        output_buffer = BasicOutputBuffer()
        dialog_context = BasicDialogContext()

        # define the model

        model = Model([
            facts,
            inferences,
            output_buffer,
            dialog_context
        ])

        # define the pipeline

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar())
        parser = BasicParser(read_grammar)

        composer = SemanticComposer(parser, query_optimizer = BasicQueryOptimizer(model))
        executor = AtomExecutor(composer, model)

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_en_us_write_grammar() + get_write_grammar())
        generator = BasicGenerator(write_grammar, model, output_buffer)

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

        tester = DialogTester(self, tests, system, logger)
        tester.run()

        print(logger)

