from typing import Callable
import unittest

from richard.ModelAdapter import ModelAdapter
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.Instance import Instance
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
from richard.semantics.commands import accept, create_np, exists, range_and
from richard.store.MemoryDb import MemoryDb
from richard.type.Simple import Simple
from richard.type.functions import Binary, Nonary, Unary


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

        db.insert(Record('country', {'id': 'mozambique', 'region': 'southern_africa', 'lat': -19, 'long': -35, 'area': 303.373, 'population': 8.820, 'capital': 'maputo', 'currency': '?'}))
        db.insert(Record('country', {'id': 'thailand', 'region': 'southeast_east', 'lat': 16, 'long': -102, 'area': 198.455, 'population': 39.950, 'capital': 'bangkok', 'currency': 'baht'}))
        db.insert(Record('country', {'id': 'congo', 'region': 'central_africa', 'lat': -1, 'long': -16, 'area': 132.46, 'population': 1.1, 'capital': 'brazzaville', 'currency': 'cfa_franc'}))

        db.insert(Record('country', {'id': 'united_states', 'region': 'north_america', 'lat': 37, 'long': 96, 'area': 3615.122, 'population': 211.210, 'capital': 'washington', 'currency': 'dollar'}))
        db.insert(Record('country', {'id': 'paraguay', 'region': 'south_america', 'lat': -23, 'long': 57, 'area': 157.47, 'population': 2.670, 'capital': 'asuncion', 'currency': 'guarani'}))

        db.insert(Record('ocean', {'id': 'indian_ocean'}))    
        db.insert(Record('ocean', {'id': 'atlantic'}))    
        db.insert(Record('ocean', {'id': 'pacific'}))            
        db.insert(Record('ocean', {'id': 'southern_ocean'}))    
        db.insert(Record('ocean', {'id': 'arctic_ocean'}))    

        db.insert(Record('borders', {'country_id1': 'afghanistan', 'country_id2': 'china'}))    
        db.insert(Record('borders', {'country_id1': 'mozambique', 'country_id2': 'indian_ocean'}))    
        db.insert(Record('borders', {'country_id1': 'china', 'country_id2': 'indian_ocean'}))    
        db.insert(Record('borders', {'country_id1': 'thailand', 'country_id2': 'indian_ocean'}))    
        db.insert(Record('borders', {'country_id1': 'congo', 'country_id2': 'atlantic'}))    

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
                    # todo: include attributes with entities, because their argument entities may be different per entity
                    attributes=[
                        Attribute("size-of", None),
                        Attribute("capital-of", "city"),
                        Attribute("location-of", "place")
                    ],
                    entities=[
                        Entity("river", [], []),
                        Entity("country", ["size-of", "capital-of", "location-of"], ["european", "asian", "american", "african"]),
                        Entity("city", ["size-of"], []),
                        Entity("ocean", [], []),
                    ], 
                    relations=[
                        Relation("borders", ['country', 'country']),
                    ], 
                )


            def interpret_relation(self, relation: str, values: list[Simple]) -> list[list[Simple]]:
                table = None
                columns = []
                if relation == "borders":
                    table = "borders"
                    columns = ["country_id1", "country_id2"]

                if not table:
                    raise Exception("No table found for " + relation)
                
                return ds.select(table, columns, values)
            

            def interpret_entity(self, entity: str) -> list[Simple]:
                return ds.select_column(entity, ['id'], [None])
            

            def interpret_attribute(self, entity: str, attribute: str, values: list[Simple]) -> list[Simple]:
                table = None
                if attribute == "capital-of":
                    table = "country"
                    columns = ["capital", "id"]
                if attribute == "size-of":
                    table = "country"
                    columns = ["area", "id"]
                if attribute == "location-of":
                    table = "country"
                    columns = ["region", "id"]

                if not table:
                    raise Exception("No table found for " + attribute)

                return ds.select(table, columns, values)
            

            def interpret_modifier(self, entity: str, modifier: str, value: Simple) -> list[Simple]:
                table = None
                if entity == "country":
                    if modifier in ["european", "asian", "african", "american"] :
                        table = "country"
                        columns = ["id", "region"]
                        regions = {
                            "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
                            "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
                            "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
                            "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
                        }

                        ids = []
                        for region in regions[modifier]:
                            ids += ds.select_column(table, columns, [value, region])
                        return ids
                    
                if not table:
                    raise Exception("No table found for " + entity + ":" + modifier)

                return ds.select_column(table, columns, [value])
                      

        model = Model(Chat80Adapter())


        # grammar

        def do_np_relative_clause(np: Nonary, relative_clause: Unary):
            return create_np(exists, lambda: np(relative_clause))
        

        def do_relative_clause_relative_clause(np: callable, relative_clause1: Unary, relative_clause2: Unary):
            return create_np(exists, lambda: range_and(np(relative_clause1), np(relative_clause2)))
        

        def do_that_vp_no_sub(vp_no_sub: callable):
            return vp_no_sub
        

        # stappenplan
        # 1 create function
        # 2 create lambda function that calls funciton #1 with the simplest of parameters (no ())
        # 3 implement #1

        grammar = [
            { "syn": "s -> 'what' 'is' np '?'", "sem": lambda np: lambda: np() },
            { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar() },
            { "syn": "s -> 'where' 'is' np '?'", "sem": lambda np: lambda: model.find_attribute_values('location-of', np) },
            { "syn": "s -> 'which' nbar 'are' adjp '?'", "sem": lambda nbar, adjp: lambda: adjp(nbar()) },
            { "syn": "s -> 'which' 'is' np '?'", "sem": lambda np: lambda: np() },
            { "syn": "s -> 'which' 'country' \''\' 's' 'capital' 'is' np '?'", "sem": lambda np: 
                lambda: model.find_attribute_objects('capital-of', np) },
            { "syn": "s -> 'does' np vp_no_sub '?'",  "sem": lambda np, vp_no_sub: lambda: np(vp_no_sub) },
            { "syn": "s -> 'how' 'large' 'is' np '?'",  "sem": lambda np: lambda: model.find_attribute_values('size-of', np) },

            { "syn": "vp_no_sub -> tv np", "sem": lambda tv, np: lambda subject: np(tv(subject)) },

            { "syn": "tv -> 'border'", "sem": lambda: 
                lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },
            { "syn": "tv -> 'borders'", "sem": lambda: 
                lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },

            { "syn": "np -> nbar", "sem": lambda nbar: create_np(exists, nbar) },
            { "syn": "np -> det nbar", "sem": lambda det, nbar: create_np(det, nbar) },
            { "syn": "np -> np relative_clause", "sem": lambda np, relative_clause: do_np_relative_clause(np, relative_clause) },
            { "syn": "np -> np relative_clause 'and' relative_clause", "sem": lambda np, rc1, rc2: do_relative_clause_relative_clause(np, rc1, rc2) },

            { "syn": "relative_clause -> 'that' vp_no_sub", "sem": lambda vp_no_sub: do_that_vp_no_sub(vp_no_sub) },

            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "nbar -> adj noun", "sem": lambda adj, noun: lambda: adj(noun()) },
            { "syn": "nbar -> attr np", "sem": lambda attr, np: lambda: attr(np) },
            { "syn": "nbar -> superlative nbar", "sem": lambda superlative, nbar: lambda: superlative(nbar()) },
            { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },

            { "syn": "superlative -> 'largest'", "sem": lambda: lambda range: model.find_entity_with_highest_attribute_value(range, 'size-of') },
            { "syn": "superlative -> 'smallest'", "sem": lambda: lambda range: model.find_entity_with_lowest_attribute_value(range, 'size-of') },

            { "syn": "det -> 'the'", "sem": lambda: exists },

            { "syn": "adjp -> adj", "sem": lambda adj: lambda range: adj(range) },

            { "syn": "adj -> 'european'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'european') },
            { "syn": "adj -> 'african'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'african') },
            { "syn": "adj -> 'american'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'american') },
            { "syn": "adj -> 'asian'", "sem": lambda: lambda range: model.filter_entities_by_modifier(range, 'asian') },

            { "syn": "noun -> 'rivers'", "sem": lambda: lambda: model.get_entity_range('river') },
            { "syn": "noun -> 'country'", "sem": lambda: lambda: model.get_entity_range('country') },
            { "syn": "noun -> 'countries'", "sem": lambda: lambda: model.get_entity_range('country') },
            { "syn": "noun -> 'ocean'", "sem": lambda: lambda: model.get_entity_range('ocean') },

            { "syn": "attr -> 'capital' 'of'", "sem": lambda: lambda np: model.find_attribute_values('capital-of', np) },

            # todo
            { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: [Instance('country', 'afghanistan')] },
            { "syn": "proper_noun -> 'china'", "sem": lambda: lambda:  [Instance('country', 'china')] },
            { "syn": "proper_noun -> 'upper_volta'", "sem": lambda: lambda:  [Instance('country', 'upper_volta')] },
            { "syn": "proper_noun -> 'london'", "sem": lambda: lambda:  [Instance('city', 'london')]  },
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
            ["What rivers are there?", [Instance(entity='river', id='amazon'), Instance(entity='river', id='brahmaputra')]],
            ["Does Afghanistan border China?", [Instance(entity='country', id='afghanistan')]],
            ["What is the capital of Upper_Volta?", [Instance(entity='city', id='ouagadougou')]],
            # missing
            ["Where is the largest country?", [Instance(entity='place', id='far_east')]],
            ["Which countries are European?", [Instance(entity='country', id='united_kingdom'), Instance(entity='country', id='albania')]],
            # err
            ["Which country's capital is London?", [Instance(entity='city', id='united_kingdom')]],
            ["Which is the largest african country?", [Instance(entity='country', id='mozambique')]],
            ["How large is the smallest american country?", [157.47]],
            ["What is the ocean that borders African countries?", [Instance(entity='ocean', id='atlantic'), Instance(entity='ocean', id='indian_ocean')]],
            ["What is the ocean that borders African countries and that borders Asian countries?", [Instance(entity='ocean', id='indian_ocean')]],
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
            
