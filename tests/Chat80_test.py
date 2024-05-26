import unittest

from richard.ModelAdapter import ModelAdapter
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.Modifier import Modifier
from richard.entity.Attribute import Attribute
from richard.entity.Range import Range
from richard.entity.Entity import Entity
from richard.entity.Relation import Relation
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.store.Record import Record
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.semantics.commands import exists, dnp
from richard.store.MemoryDb import MemoryDb
from richard.type.Simple import Simple


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

        # fill an in-memory database

        db = MemoryDb()
        db.insert(Record('river', {'id': 'amazon'}))
        db.insert(Record('river', {'id': 'brahmaputra'}))
       
        db.insert(Record('country', {'id': 'afghanistan', 'region': 'indian_subcontinent', 'lat': 33, 'long': -65, 'area': 254.861, 'population': 18.290, 'capital': 'kabul', 'currency': 'afghani'}))
        db.insert(Record('country', {'id': 'china', 'region': 'far_east', 'lat': 30, 'long': -110, 'area': 3691.502, 'population': 840.0, 'capital': 'peking', 'currency': 'yuan'}))
        db.insert(Record('country', {'id': 'upper_volta', 'region': 'west_africa', 'lat': 12, 'long': 2, 'area': 105.869, 'population': 5.740, 'capital': 'ouagadougou', 'currency': 'cfa_franc'}))       
        db.insert(Record('country', {'id': 'rwanda', 'region': 'central_africa', 'lat': -2, 'long':-30, 'area': 10.169, 'population': 3.980, 'capital': 'kigali', 'currency': 'rwanda_franc'}))       
        db.insert(Record('country', {'id': 'albania', 'region': 'southern_europe', 'lat': 41, 'long': -20, 'area': 11.100, 'population': 2.350, 'capital': 'tirana', 'currency': 'lek'}))
        db.insert(Record('country', {'id': 'united_kingdom', 'region': 'western_europe', 'lat': 54, 'long': 2, 'area': 94.209, 'population': 55.930, 'capital': 'london', 'currency': 'pound'}))
        
        db.insert(Record('borders', {'country_id1': 'afghanistan', 'country_id2': 'china'}))    

        # create an adapter for this data source

        ds = MemoryDbDataSource(db)

        # model

        class Chat80Adapter(ModelAdapter):
            def __init__(self) -> None:
                super().__init__(
                    modifiers=[
                        Modifier("european"),
                        Modifier("asian"),
                        Modifier("american"),
                        Modifier("african"),
                    ],
                    attributes=[
                        Attribute("size-of"),
                        Attribute("capital-of"),
                        Attribute("location-of")
                    ],
                    entities=[
                        Entity("river", [], []),
                        Entity("country", ["size-of", "capital-of", "location-of"], ["european", "asian", "american", "african"]),
                        Entity("city", ["size-of"], []),
                    ], 
                    relations=[
                        Relation("borders", ['country', 'country']),
                    ], 
                )


            def interpret_relation(self, relation_name: str, values: list[Simple]) -> list[list[Simple]]:
                columns = []
                if relation_name == "borders":
                    table = "borders"
                    columns = ["country_id1", "country_id2"]

                return ds.select(table, columns, values)
            

            def interpret_entity(self, entity_name: str) -> list[Simple]:
                return ds.select_column(entity_name, ['id'], [None])
            

            def interpret_attribute(self, entity_name: str, attribute_name: str, values: list[Simple]) -> list[Simple]:
                if attribute_name == "capital-of":
                    table = "country"
                    columns = ["capital", "id"]
                if attribute_name == "size-of":
                    table = "country"
                    columns = ["area", "id"]
                if attribute_name == "location-of":
                    table = "country"
                    columns = ["region", "id"]

                return ds.select(table, columns, values)
            

            def interpret_modifier(self, entity_name: str, modifier_name: str, value: Simple) -> list[Simple]:
                if entity_name == "country":
                    if modifier_name in ["european", "asian", "african", "american"] :
                        table = "country"
                        columns = ["id", "region"]
                        regions = {
                            "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
                            "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
                            "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
                            "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
                        }

                        ids = []
                        for region in regions[modifier_name]:
                            ids += ds.select_column(table, columns, [value, region])
                        return ids

                return ds.select_column(table, columns, [value])
                      

        model = Model(Chat80Adapter())


        # grammar

        grammar = [
            { "syn": "s -> 'what' 'is' np '?'", "sem": lambda np: lambda: model.filter_entities(np()) },
            { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar() },
            { 
                "syn": "s -> 'where' 'is' np '?'", 
                "sem": lambda np: lambda: model.find_attribute_values('location-of', np())
            },
            { "syn": "s -> 'which' nbar 'are' adjp '?'", "sem": lambda nbar, adjp: lambda: adjp(nbar()) },
            { "syn": "s -> 'which' 'is' np '?'", "sem": lambda np: lambda: model.filter_entities(np()) },
            { "syn": "s -> 'which' 'country' \''\' 's' 'capital' 'is' nbar '?'", "sem": lambda nbar: 
                lambda: model.find_attribute_objects('capital-of', dnp(exists, nbar)) },
            { "syn": "s -> 'does' np vp_no_sub '?'",  "sem": lambda np, vp_no_sub: lambda: model.filter_entities(np(), vp_no_sub) },

            { "syn": "vp_no_sub -> tv np", "sem": lambda tv, np: lambda subject: model.filter_entities(np(), tv(subject)) },

            { "syn": "tv -> 'border'", "sem": lambda: 
                lambda subject: lambda object: model.find_relation_values('borders', [subject, object]) },

            { "syn": "np -> nbar", "sem": lambda nbar: lambda: dnp(exists, nbar) },
            { "syn": "np -> det nbar", "sem": lambda det, nbar: lambda: dnp(det, nbar) },

            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "nbar -> adj noun", "sem": lambda adj, noun: lambda: adj(noun()) },
            { "syn": "nbar -> attr np", "sem": lambda attr, np: lambda: attr(np) },
            { "syn": "nbar -> superlative nbar", "sem": lambda superlative, nbar: lambda: superlative(nbar()) },

            { "syn": "superlative -> 'largest'", "sem": lambda: lambda range: model.find_entity_with_highest_attribute_value(range, 'size-of') },

            { "syn": "det -> 'the'", "sem": lambda: exists },

            { "syn": "adjp -> adj", "sem": lambda adj: lambda range: adj(range) },

            { "syn": "adj -> 'european'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'european') },
            { "syn": "adj -> 'african'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'african') },
            { "syn": "adj -> 'american'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'american') },
            { "syn": "adj -> 'asian'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'asian') },

            { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },
            { "syn": "noun -> 'rivers'", "sem": lambda: lambda: model.get_entity_range('river') },
            { "syn": "noun -> 'country'", "sem": lambda: lambda: model.get_entity_range('country') },
            { "syn": "noun -> 'countries'", "sem": lambda: lambda: model.get_entity_range('country') },

            { "syn": "attr -> 'capital' 'of'", "sem": lambda: lambda np: model.find_attribute_values('capital-of', np()) },

            # todo
            { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: Range('country', ['afghanistan']) },
            { "syn": "proper_noun -> 'china'", "sem": lambda: lambda: Range('country', ['china']) },
            { "syn": "proper_noun -> 'upper_volta'", "sem": lambda: lambda: Range('country', ['upper_volta']) },
            { "syn": "proper_noun -> 'london'", "sem": lambda: lambda: Range('city', ['london']) },
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
            ["What rivers are there?", ['amazon', 'brahmaputra']],
            ["Does Afghanistan border China?", ['afghanistan']],
            ["What is the capital of Upper_Volta?", ["ouagadougou"]],
            ["Where is the largest country?", ["far_east"]],
            ["Which countries are European?", ["albania", "united_kingdom"]],
            ["Which country's capital is London?", ["united_kingdom"]],
            ["Which is the largest african country?", ['upper_volta']],
            ["How large is the smallest american country?", []]
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
