from richard.core.Logger import Logger
from richard.entity.GrammarRules import GrammarRules
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeParseTreeSortHeuristics import SomeParseTreeSortHeuristics
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.tokenizer.BasicTokenizerProduct import BasicTokenizerProduct
from richard.type.SimpleGrammar import SimpleGrammar
from .tree_sort_heuristics.BasicParseTreeSortHeuristics import BasicParseTreeSortHeuristics
from .helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from .earley.EarleyParser import EarleyParser


class BasicParser(SomeProcessor):

    grammar: GrammarRules
    parser: EarleyParser
    tree_sorter: SomeParseTreeSortHeuristics


    def __init__(self, grammar: GrammarRules) -> None:
        self.grammar = grammar
        self.parser = EarleyParser()
        self.tree_sorter = BasicParseTreeSortHeuristics()


    def get_name(self) -> str:
        return "Parser"


    def process(self, request: SentenceRequest) -> ProcessResult:
        result = self.parser.parse(self.grammar, request.text)
        sorted_trees = self.tree_sorter.sort_trees(result.products)
        products = [BasicParserProduct(tree) for tree in sorted_trees]
        return ProcessResult(
            products,
            result.error
        )



