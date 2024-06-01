import unittest

from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.Instance import Instance
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.semantics.commands import create_np, exists
from .chat80.chat80_model import model

class TestChat80(unittest.TestCase):
    """
    Mimics a Chat80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    Topics:
    - attributes ('capital of')
    - superlatives ('largest')
    - extraposition (long distance despendencies)
    - relative clauses
    """
   
    def test_chat80(self):

        grammar = [
            { "syn": "s -> 'what' 'are' 'the' attr 'of' np '?'", "sem": lambda attr, np: lambda: model.create_attribute_map(np, attr) },

            { "syn": "s -> 'what' 'is' np '?'", "sem": lambda np: lambda: np() },
            { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar() },
            { "syn": "s -> 'where' 'is' np '?'", "sem": lambda np: lambda: model.find_attribute_values(lambda: 'location-of', np) },
            { "syn": "s -> 'which' nbar 'are' adjp '?'", "sem": lambda nbar, adjp: lambda: adjp(nbar) },
            { "syn": "s -> 'which' 'is' np '?'", "sem": lambda np: lambda: np() },
            { "syn": "s -> 'which' 'country' \''\' 's' attr 'is' np '?'", "sem": lambda attr, np: 
                lambda: model.find_attribute_objects(attr, np) },
            { "syn": "s -> 'does' np vp_no_sub '?'",  "sem": lambda np, vp_no_sub: lambda: np(vp_no_sub) },
            { "syn": "s -> 'how' 'large' 'is' np '?'",  "sem": lambda np: lambda: model.find_attribute_values(lambda: 'size-of', np) },

            { "syn": "vp_no_sub -> tv np", "sem": lambda tv, np: lambda subject: np(tv(subject)) },

            { "syn": "tv -> 'border'", "sem": lambda: 
                lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },
            { "syn": "tv -> 'borders'", "sem": lambda: 
                lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },
            { "syn": "tv -> 'bordering'", "sem": lambda: 
                lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },

            { "syn": "np -> nbar", "sem": lambda nbar: create_np(exists, nbar) },
            { "syn": "np -> det nbar", "sem": lambda det, nbar: create_np(det, nbar) },
            { "syn": "np -> np relative_clause", "sem": lambda np, relative_clause: create_np(exists, lambda: np(relative_clause)) },
            { "syn": "np -> np relative_clause 'and' relative_clause", "sem": lambda np, rc1, rc2: create_np(exists, lambda: np(rc1) & np(rc2)) },

            { "syn": "relative_clause -> 'that' vp_no_sub", "sem": lambda vp_no_sub: lambda subject: vp_no_sub(subject) },
            { "syn": "relative_clause -> vp_no_sub", "sem": lambda vp_no_sub: lambda subject: vp_no_sub(subject) },

            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "nbar -> adj noun", "sem": lambda adj, noun: lambda: adj(noun) },
            { "syn": "nbar -> attr 'of' np", "sem": lambda attr, np: lambda: model.find_attribute_values(attr, np) },
            { "syn": "nbar -> superlative nbar", "sem": lambda superlative, nbar: lambda: superlative(nbar) },

            { "syn": "superlative -> 'largest'", "sem": lambda: lambda range: model.find_entity_with_highest_attribute_value(range, 'size-of') },
            { "syn": "superlative -> 'smallest'", "sem": lambda: lambda range: model.find_entity_with_lowest_attribute_value(range, 'size-of') },

            { "syn": "det -> 'the'", "sem": lambda: exists },

            { "syn": "adjp -> adj", "sem": lambda adj: lambda range: adj(range) },

            { "syn": "adj -> 'european'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'european') },
            { "syn": "adj -> 'african'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'african') },
            { "syn": "adj -> 'american'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'american') },
            { "syn": "adj -> 'asian'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'asian') },

            { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },
            { "syn": "noun -> 'rivers'", "sem": lambda: lambda: model.get_instances('river') },
            { "syn": "noun -> 'country'", "sem": lambda: lambda: model.get_instances('country') },
            { "syn": "noun -> 'countries'", "sem": lambda: lambda: model.get_instances('country') },
            { "syn": "noun -> 'ocean'", "sem": lambda: lambda: model.get_instances('ocean') },

            { "syn": "attr -> 'capital'", "sem": lambda: lambda: 'capital-of' },
            { "syn": "attr -> 'capitals'", "sem": lambda: lambda: 'capital-of' },

            # todo
            { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: set([Instance('country', 'afghanistan')]) },
            { "syn": "proper_noun -> 'china'", "sem": lambda: lambda:  set([Instance('country', 'china')]) },
            { "syn": "proper_noun -> 'upper_volta'", "sem": lambda: lambda:  set([Instance('country', 'upper_volta')]) },
            { "syn": "proper_noun -> 'london'", "sem": lambda: lambda:  set([Instance('city', 'london')])  },
            { "syn": "proper_noun -> 'baltic'", "sem": lambda: lambda:  set([Instance('sea', 'baltic')])  },
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
            ["What rivers are there?", set([Instance(entity='river', id='amazon'), Instance(entity='river', id='brahmaputra')])],
            ["Does Afghanistan border China?", set([Instance(entity='country', id='afghanistan')])],
            ["What is the capital of Upper_Volta?", set([Instance(entity='city', id='ouagadougou')])],
            ["Where is the largest country?", set([Instance(entity='place', id='far_east')])],
            ["Which countries are European?", set([Instance(entity='country', id='united_kingdom'), Instance(entity='country', id='albania'), Instance(entity='country', id='poland')])],
            ["Which country's capital is London?", set([Instance(entity='country', id='united_kingdom')])],
            ["Which is the largest african country?", set([Instance(entity='country', id='mozambique')])],
            ["How large is the smallest american country?", set([157.47])],
            ["What is the ocean that borders African countries?", set([Instance(entity='ocean', id='atlantic'), Instance(entity='ocean', id='indian_ocean')])],
            ["What is the ocean that borders African countries and that borders Asian countries?", set([Instance(entity='ocean', id='indian_ocean')])],
            ["What are the capitals of the countries bordering the Baltic?", [[Instance(entity='country', id='poland'), 'warsaw']]],
            ["Which countries are bordered by two seas?", []]
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
            
