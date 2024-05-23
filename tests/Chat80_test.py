import unittest

from richard.ModelAdapter import ModelAdapter
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.Attribute import Attribute
from richard.entity.Range import Range
from richard.entity.Entity import Entity
from richard.entity.Relation import Relation
from richard.store.Record import Record
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.semantics.commands import exists, filter, dnp
from richard.store.MemoryDb import MemoryDb


class TestChat80(unittest.TestCase):
    """
    Mimics a Chat80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    Topics:
    - attributes ('capital of')
    - aggregation ('largest')
    - extraposition (long distance despendencies)
    - relative clauses
    """
   
    def test_chat80(self):

        # an in-memory database

        db = MemoryDb()
        db.insert(Record('river', {'id': 'amazon'}))
        db.insert(Record('river', {'id': 'brahmaputra'}))
       
        db.insert(Record('country', {'id': 'afghanistan', 'region': 'indian_subcontinent', 'lat': 33, 'long': -65, 'area': 254.861, 'population': 18.290, 'capital': 'kabul', 'currency': 'afghani'}))
        db.insert(Record('country', {'id': 'china', 'region': 'far_east', 'lat': 30, 'long': -110, 'area': 3691.502, 'population': 840.0, 'capital': 'peking', 'currency': 'yuan'}))
        db.insert(Record('country', {'id': 'upper_volta', 'region': 'west_africa', 'lat': 12, 'long': 2, 'area': 105.869, 'population': 5.740, 'capital': 'ouagadougou', 'currency': 'cfa_franc'}))

        db.insert(Record('borders', {'country_id1': 'afghanistan', 'country_id2': 'china'}))    

        # data store adapter
        # todo

        # model

        class Chat80Adapter(ModelAdapter):
            def __init__(self) -> None:
                super().__init__(
                    attributes=[
                        Attribute("size"),
                        Attribute("capital")
                    ],
                    entities=[
                        Entity("river", [], ["big"]),
                        Entity("country", ["size", "capital"], ["big"]),
                        Entity("city", ["size"], ["big"]),
                    ], 
                    relations=[
                        Relation("borders", ['country', 'country']),
                    ], 
                )


            def interpret_relation(self, relation_name: str, values: list[any]):
                columns = []
                if relation_name == "borders":
                    table = "borders"
                    columns = ["country_id1", "country_id2"]

                where = {}
                for i, field in enumerate(values):
                    if field is not None:
                        column = columns[i]
                        where[column] = field

                return db.select(Record(table, where)).fields(columns)
            

            def interpret_entity(self, entity_name: str):
                return Range(entity_name, db.select(Record(entity_name)).field('id'))
            

            def interpret_attribute(self, entity_name: str, attribute_name: str, values: list[any]):
                if entity_name == "country":
                    if attribute_name == "capital":
                        table = "country"
                        columns = ["capital", "id"]
                    if attribute_name == "size":
                        table = "country"
                        columns = ["area", "id"]

                where = {}
                for i, field in enumerate(values):
                    if field is not None:
                        column = columns[i]
                        where[column] = field

                print(table, where, columns)

                return db.select(Record(table, where)).fields(columns)


        model = Model(Chat80Adapter())


        # grammar

        grammar = [
            { "syn": "s -> 'what' 'is' np '?'", "sem": lambda np: lambda: filter(np()) },
            { 
                "syn": "s -> 'where' 'is' np '?'", 
                "sem": lambda np: lambda: filter(np()) # todo: where?!
            },
            { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar() },
            { "syn": "s -> 'does' np vp_no_sub '?'",  "sem": lambda np, vp_no_sub: lambda: filter(np(), vp_no_sub) },
            { "syn": "vp_no_sub -> tv np", "sem": lambda tv, np: lambda subject: filter(np(), tv(subject)) },
            { "syn": "np -> nbar", "sem": lambda nbar: lambda: dnp(exists, nbar) },
            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "np -> det nbar", "sem": lambda det, nbar: lambda: dnp(det, nbar) },
            { "syn": "nbar -> attr np", "sem": lambda attr, np: lambda: attr(np) },

            { "syn": "nbar -> superlative nbar", "sem": lambda superlative, nbar: lambda: superlative(nbar()) },
            { "syn": "superlative -> 'largest'", "sem": lambda: lambda range: model.find_max(range, 'size') },

            { "syn": "det -> 'the'", "sem": lambda: exists },
            { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },
            { "syn": "noun -> 'rivers'", "sem": lambda: lambda: model.get_range('river') },
            { "syn": "noun -> 'country'", "sem": lambda: lambda: model.get_range('country') },
            { "syn": "tv -> 'border'", "sem": lambda: 
                lambda subject: 
                    lambda object: 
                        model.relation_exists('borders', [subject, object]) },

            { "syn": "attr -> 'capital' 'of'", "sem": lambda: lambda np: model.search_attribute('capital', np()) },

            # todo
            { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: Range('country', ['afghanistan']) },
            { "syn": "proper_noun -> 'china'", "sem": lambda: lambda: Range('country', ['china']) },
            { "syn": "proper_noun -> 'upper_volta'", "sem": lambda: lambda: Range('country', ['upper_volta']) },
        ]

        # pipeline

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = SemanticExecutor(composer)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor)
        ])

        # testing

        tests = [
            # ["What rivers are there?", ['amazon', 'brahmaputra']],
            # ["Does Afghanistan border China?", ['afghanistan']],
            # ["What is the capital of Upper_Volta?", ["ouagadougou"]],
            ["Where is the largest country?", ["far_east"]]
        ]

        for test in tests:
            question, answer = test
            request = SentenceRequest(question)
            result = pipeline.enter(request)

            if not result.error_code == "":
                print(result.error_code, result.error_args) 
                break

            results = executor.get_results(request)
            self.assertEqual(set(answer), set(results))
