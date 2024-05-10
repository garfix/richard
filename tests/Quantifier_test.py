import unittest

from lib.Pipeline import Pipeline
from lib.entity.ParseTreeNode import ParseTreeNode
from lib.entity.Record import Record
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.parser.BasicParser import BasicParser
from lib.processor.semantic_composer.SemanticComposer import SemanticComposer
from lib.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer
from lib.store.MemoryDb import MemoryDb



# def find(quant: tuple[ParseTreeNode, ParseTreeNode], vp: ParseTreeNode) -> list:
#     print('find')
#     qp, nbar = quant
#     elements = nbar.sem(nbar)
#     range_count = len(elements)

#     result = []
#     for element in elements:
#         for e2 in vp.sem(element):
#             result.append(e2)
#     result_count = len(result)
#     quantifier = qp()
#     if quantifier(result_count, range_count):
#         return result
#     else:
#         return []

def find(quant: tuple[callable, callable], vp: callable) -> list:
    print('find', vp)
    qp, nbar = quant
    elements = nbar()
    range_count = len(elements)

    print('s-------')
    result = []
    for element in elements:
        for e2 in vp(element):
            result.append(e2)
    result = list(set(result))
    result_count = len(result)
    print('e-------')
    print(result_count, result)
    if qp(result_count, range_count):
        print('correct number')
        return result
    else:
        print('wrong number')
        return []

db = MemoryDb()
db.assert_record(Record('has_child', {'parent': 'mary', 'child': 'lucy'}))
db.assert_record(Record('has_child', {'parent': 'mary', 'child': 'bonny'}))
db.assert_record(Record('has_child', {'parent': 'barbara', 'child': 'john'}))
db.assert_record(Record('has_child', {'parent': 'barbara', 'child': 'chuck'}))
db.assert_record(Record('has_child', {'parent': 'william', 'child': 'oswald'}))
db.assert_record(Record('has_child', {'parent': 'william', 'child': 'bertrand'}))

# qp => dp, detp?

def s(np, vp_no_sub_a): 
    return lambda: find(np(), vp_no_sub_a)

def has_child(aux, qp, parent):
    return lambda sub: find(
        (qp, parent),
        lambda obj: list(set([r.values['child'] for r in db.match(Record('has_child', {'parent': sub, 'child': obj}))])))

class TestQuantifier(unittest.TestCase):
   
    def test_quantifier(self):


        grammar = [
            { "syn": "s -> np vp_no_sub", "sem": s },
            { "syn": "vp_no_sub -> aux qp child", "sem": has_child },
            { "syn": "np -> qp nbar", "sem": lambda qp, nbar: lambda: (qp, nbar) },
            { "syn": "qp -> quantifier", "sem": lambda quantifier: lambda result, range: quantifier(result, range) },
            { "syn": "quantifier -> det", "sem": lambda det: lambda result, range: det(result, range) },
            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "det -> 'every'", "sem": lambda: lambda result, range: result == range },
            { "syn": "det -> number", "sem": lambda number: lambda result, range: result == number() },
            { "syn": "number -> 'two'", "sem": lambda: lambda: 2 },
            { "syn": "noun -> 'parent'", "sem": lambda: lambda: list(set([r.values['parent'] for r in db.match(Record('has_child', {}))])) },
            { "syn": "child -> 'children'", "sem": lambda: lambda: list(set([r.values['child'] for r in db.match(Record('has_child', {}))])) },
            { "syn": "aux -> 'has'", "sem": lambda: lambda: None },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = SemanticExecutor(composer)

        pipeline = Pipeline([
            tokenizer,
            parser,
            composer,
            executor
        ])



        # grammar = [
        #     { "syn": "s -> np vp_no_sub", "sem": lambda node: find(node.child("np").sem(node.child("np")), node.child("vp_no_sub")) },
        #     { "syn": "vp_no_sub -> aux qp child", "sem": lambda node: find(
        #         (node.child('qp'), node.child['child']),
        #         lambda parent: [r.values['child'] for r in db.match('has_child', {'parent': parent})]
        #     ) },
        #     { "syn": "np -> qp nbar", "sem": lambda node: (node.child('qp'), node.child('nbar')) },
        #     { "syn": "qp -> quantifier", "sem": lambda node: node.child("quantifier") },
        #     { "syn": "quantifier -> det", "sem": lambda node: node.child("det") },
        #     { "syn": "nbar -> noun", "sem": lambda node: node.child("noun") },
        #     { "syn": "det -> 'every'", "sem": lambda node: lambda result, range: result == range },
        #     { "syn": "det -> number", "sem": lambda node: lambda result, range: result == node.child('number').sem() },
        #     { "syn": "number -> 'two'", "sem": lambda: 2 },
        #     { "syn": "noun -> 'parent'", "sem": lambda: list(set([r.values['parent'] for r in db.match('has_child', {})])) },
        #     { "syn": "child -> 'children'", "sem": lambda: list(set([r.values['child'] for r in db.match('has_child', {})])) },
        #     { "syn": "aux -> 'has'", "sem": None },
        # ]

        # tokenizer = BasicTokenizer()
        # parser = BasicParser(grammar, tokenizer)
        # executor = SemanticExecutor(parser)

        # pipeline = Pipeline([
        #     tokenizer,
        #     parser,
        #     executor
        # ])

        request = SentenceRequest("Every parent has two children")
        pipeline.enter(request)

        result = request.get_current_product(parser)
        # print(result)

        result = request.get_alternative_products(executor)
        print("result: ", result)
        # self.assertEqual(len(result), 3)

    