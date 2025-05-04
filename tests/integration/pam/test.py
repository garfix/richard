import unittest
import pathlib

from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.DialogTester import DialogTester
from richard.core.Logger import Logger
from richard.entity.SentenceRequest import SentenceRequest
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
from .PAMDB import PAMDB
from .PAMModule import PAMModule
from .read_grammar import get_read_grammar
from .write_grammar import get_write_grammar


class TestPAM(unittest.TestCase):
    """
    A basic application that creates a test and shows how to interact with the system.
    """

    def test_pam(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        # define the database

        db = PAMDB()
        facts = PAMModule(db)

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

        # test the system

        tests = [
            ["Hello world", "Hi there!"],

            # 1.1 Introduction; 1.4 Goals
            ["One day, John went through a red light and was pulled over. John had just gotten a summons for speeding by a cop the previous week, and was told that if he got another violation, his license would be taken away. Then John remembered that he had two tickets for the Giants' game on him. He told the cop that he would give them to him if he would forget the whole incident. The cop happened to be a terrific football fan . Re took John's tickets and drove away.", "OK"],
            ["Why did John offer the cop a couple of tickets?", "Because he was afraid he was going to lose his license if he got another summons."],

            # 1.2 PAM; 1.7 A PAM Example
            ["John wanted money. He got a gun and walked into the liquor store. He told the owner he wanted some money. The owner gave John the money and John left.", "OK"],
            ["Why did John get a gun?", "Because John wanted to rob the liquor store."],
            ["Why did John threaten the shopkeeper?", "Because John needed to get some money."],
            ["Why did the shopkeeper give John the money?", "Because the shopkeeper didn't want to get hurt."],
            ["Why did John leave?", "Because John didn't want to get caught."],
            ["What were the consequences of John getting a gun?", "John had a weapon which enabled him to rob the liquor store."],
            ["What were the consequences of John threatening the shopkeeper?", "The shopkeeper didn't want to get hurt so he gave John the money."],
            ["What were the consequences of the shopkeeper giving John the money?", "John had some money."],
            ["How did John go to the liquor store?", "John walked to the liquor store."],
            ["How did John threaten the shopkeeper?", "John got a gun and he walked to the liquor store."],
            ["How did John leave?", "John walked."],
            ["Story from John's point of view", "I needed to get some dough. So I got myself this gun, and I walked down to the liquor store. I told the shopkeeper that if he didn't let me have the money then I would shoot him. So he handed it over. Then he left."],
            ["Story from the owner's point of view", "I was minding the store when a man entered . He threatened me with a gun and demanded all the cash receipts. W ell. I didn't want to get hurt, so I gave him the money. Then he escaped."],

            # 1.2 PAM (2) and 11.2.2 Computer example
            ["Willa was hungry. She picked up the Michelin guide and got into her car.", "OK"],
            ["Why did Willa pick up the Michelin Guide?" , "Because Willa wanted to know where a restaurant was."],
            ["Why did Wi lla get into her car?", "Because Willa wanted to get to a restaurant."],
            ["What we re the consequences of Willa picking up the Michelin Guide?", "This enabled Willa to read the Michelin Guide."],
            ["What were the consequences of Willa getting into her automobile?", "This enabled Willa to drive somewhere."],
            ["How did Willa get into her car?", "Wila walked to her automobile."],
            ["The story from Willa's point of view", "I wanted to get something to eat, but I didn't know where a restaurant was. So I picked up the Michelin Guide and I got into my car."],

            # 1.2 PAM (3); 5.3 Goal subsumption state replacement
            ["John and Mary were married. Then one day, John was killed in a car accident. Mary had to get a job.", "OK"],
            ["Why did Mary need employment?", "John died and so she needed a source of money."],

            # 1.2 PAM (4); 1.6 What this thesis is about; 7.3.1.2 Computer example
            ["John wanted to watch the football game, but he had a paper due the next day. John watched the football game. He failed civics.", "OK"],
            ["Why did John fail a course in Civics?", "He failed to hand in an assignment"],

            # 2.2 Sample story
            ["John wan ted Bill's bicycle. He walked over to Bill and asked him if he would give it to him. Bill refused. Bill he would give him five dolla rs for it, but Bill would not agree. but Bill would not agree. John told Bill he would break his arm if he didn ’t let him have it. Bill let John have the bicycle.", "OK"],
            ["Why did John walk over to Bill?", "Because he wan ted to get his bicycle."],
            ["Why did Bill give his bicycle to John", "Because he didn't want to get hurt."],
            ["What were the consequences of John's walking over to Bill?", "This enabled him to ask him to give him Bill's bicycle."],
            ["What were the consequences of John's asking Bill to give him Bill's bicycle?", "Bill told him that Bill wouldn't give hiw Bill's bicycle."],
            ["Tell the story from John's point of view", "I wanted to get Bill's bicycle. So I walked over to him, and I asked him to hand it over. He told me that he wouldn't hand it over. So I asked him to sell It to me for five dollars. Then he told me that he wouldn't hand over his bicycle. I told him that If he didn't hand it over then I would break his arm. He handed over his bicycle."],
            ["Tell the story from Bill's point of view", "John came over. He asked me to give him my bicycle. I wanted to keep the bicycle, so I told him that I wouldn't give it to him. Then he offered to buy it for five bucks. I wanted to keep the bicycle , so I told him that I wouldn't give it to him . He told me that if I didn't give it to him then he would break my arm. I didn't want to get hurt. So I gave him my bicycle."],

            # 5.2 Goal subsumption state establishment
            ["John loved drinking hot coffee. He bought a thermos.", "OK"],
            ["Why did John buy a thermos?", "So he could enjoy drinking hot coffee whenever he wanted to."],

            # 7.3.1.1 Factors involved in time-based goal conflicts
            ["John had just enough money to buy either a stereo or a television, but he only had enough money for one. John bought a stereo and stole a television set.", "OK"],
            ["Why did John decide to steal the television set?", "Because John no longer had enough money left to buy one."],

            # 8.1.1 Goal competition
            ["John told Mary he wanted to watch the football game. Mary said that she wanted to watch the Bolshoi ballet. Mary put on channel 3. John got out the lawnmower.", "OK"],
            ["What would have happened if Mary hadn't wanted to watch the ballet?", "John would have been able to watch the football game."],

            # 9.3.2.1 A computer example
            ["John wanted to win the stockcar race. Bill also want to win the stockcar race. Before the race John cut Bill's ignition wire.", "OK"],
            ["Why did John break an ignition wire?", "Because he was trying to prevent Bill from racing."],

            # 9.3.3.2.1 A Computer example
            ["John wanted to get the treasure, but it was guarded by a dragon. John walked over to the treasure quietly.", "OK"],
            ["Why did John sneak over to the treasure?", "Because he was trying to get the treasure and he wanted to prevent the dragon from knowing where he was."],

            # 14 A detailed example
            ["John was lost. He pulled over to a farmer standing by the side of the road. he asked him where he was.", "OK"],
            ["Why did John pull over to a farmer?", "Because he wanted to know where he was."],
            ["Why did John ask a farmer to tell him where he was?", "Because he wanted to get someplace."],
            ["What were the consequences of John's pulling over to a farmer?", "This enabled him to ask him where John was."],
            ["What happened when John pulled over to a farmer?", "He asked him to tell him where he was."],
            ["What happened when John asked a farmer to tell him where he was?", "I don't know."],
            ["How did John go over to a farmer?", "He drove over to him."]
        ]

        # comment in the following rules to see intermediate results
        return

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
