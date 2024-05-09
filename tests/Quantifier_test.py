import unittest

from lib.Pipeline import Pipeline
from lib.entity.Record import Record
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.parser.BasicParser import BasicParser
from lib.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer
from lib.store.MemoryDb import MemoryDb



def find(quant: tuple, vp: callable) -> list:
    print('find')
    qp, nbar = quant.sem()(quant)
    elements = nbar.sem(nbar)
    result = []
    for element in elements:
        for e2 in vp.sem(element):
            result.append(e2)
    result_count = len(result)
    range_count = len(elements)
    quantifier = qp()
    if quantifier(result_count, range_count):
        return result
    else:
        return []


class TestQuantifier(unittest.TestCase):
   
    def test_quantifier(self):

        db = MemoryDb()
        db.assert_record(Record('has_child', {'parent': 'mary', 'child': 'lucy'}))
        db.assert_record(Record('has_child', {'parent': 'mary', 'child': 'bonny'}))
        db.assert_record(Record('has_child', {'parent': 'barbara', 'child': 'john'}))
        db.assert_record(Record('has_child', {'parent': 'barbara', 'child': 'check'}))
        db.assert_record(Record('has_child', {'parent': 'william', 'child': 'oswald'}))
        db.assert_record(Record('has_child', {'parent': 'william', 'child': 'bertrand'}))

        # qp => dp, detp?

        grammar = [
            { "syn": "s -> np vp_no_sub", "sem": lambda node: find(node.child("np"), node.child("vp_no_sub")) },
            { "syn": "vp_no_sub -> aux qp child", "sem": lambda node: find(
                (node.child('qp'), node.child['child']),
                lambda parent: [r.values['child'] for r in db.match('has_child', {'parent': parent})]
            ) },
            { "syn": "np -> qp nbar", "sem": lambda node: (node.child('qp'), node.child('nbar')) },
            { "syn": "qp -> quantifier", "sem": lambda node: node.child("quantifier") },
            { "syn": "quantifier -> det", "sem": lambda node: node.child("det") },
            { "syn": "nbar -> noun", "sem": lambda node: node.child("noun") },
            { "syn": "det -> 'every'", "sem": lambda node: lambda result, range: result == range },
            { "syn": "det -> number", "sem": lambda node: lambda result, range: result == node.sem('number')() },
            { "syn": "number -> 'two'", "sem": lambda: 2 },
            { "syn": "noun -> 'parent'", "sem": lambda: list(set([r.values['parent'] for r in db.match('has_child', {})])) },
            { "syn": "child -> 'children'", "sem": lambda: list(set([r.values['child'] for r in db.match('has_child', {})])) },
            { "syn": "aux -> 'has'", "sem": None },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        executor = SemanticExecutor(parser)

        pipeline = Pipeline([
            tokenizer,
            parser,
            executor
        ])

        request = SentenceRequest("Every parent has two children")
        pipeline.enter(request)

        result = request.get_current_product(parser)
        # print(result)

        result = request.get_current_product(executor)
        print("result: ", result)
        # self.assertEqual(len(result), 3)

    