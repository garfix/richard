from richard.entity.GrammarRules import GrammarRules
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeParseTreeSortHeuristics import SomeParseTreeSortHeuristics
from richard.interface.SomeParser import SomeParser
from richard.interface.SomeTokenizer import SomeTokenizer
from richard.type.SimpleGrammar import SimpleGrammar
from .tree_sort_heuristics.BasicParseTreeSortHeuristics import BasicParseTreeSortHeuristics
from .helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from .earley.EarleyParser import EarleyParser


class BasicParser(SomeParser):

    tokenizer: SomeTokenizer
    grammar: GrammarRules
    parser: EarleyParser
    tree_sorter: SomeParseTreeSortHeuristics


    def __init__(self, grammar: SimpleGrammar, tokenizer: SomeTokenizer) -> None:

        self.tokenizer = tokenizer

        sgrp = SimpleGrammarRulesParser()
        self.grammar = sgrp.parse(grammar)
        self.parser = EarleyParser()
        self.tree_sorter = BasicParseTreeSortHeuristics()
            

    def process(self, request: SentenceRequest) -> ProcessResult:
        tokens = self.tokenizer.get_tokens(request)
        result = self.parser.parse(self.grammar, tokens)
        return ProcessResult(
            self.tree_sorter.sort_trees(result.products),
            result.error_code,
            result.error_args
        )
    

    def get_tree(self, request: SentenceRequest) -> ParseTreeNode:
        return request.get_current_product(self)
    
