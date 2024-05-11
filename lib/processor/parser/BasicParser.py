from lib.entity.GrammarRules import GrammarRules
from lib.entity.ParseTreeNode import ParseTreeNode
from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.SomeParser import SomeParser
from lib.interface.SomeTokenizer import SomeTokenizer
from lib.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from lib.type.SimpleGrammar import SimpleGrammar
from .earley.EarleyParser import EarleyParser


class BasicParser(SomeParser):

    tokenizer: SomeTokenizer
    grammar: GrammarRules
    parser: EarleyParser


    def __init__(self, grammar: SimpleGrammar, tokenizer: SomeTokenizer) -> None:

        self.tokenizer = tokenizer

        sgrp = SimpleGrammarRulesParser()
        self.grammar = sgrp.parse(grammar)
        self.parser = EarleyParser()
            

    def process(self, request: SentenceRequest):
        tokens = self.tokenizer.get_tokens(request)
        result = self.parser.parse(self.grammar, tokens)
        return result.trees
    

    def get_tree(self, request: SentenceRequest) -> ParseTreeNode:
        return request.get_current_product(self)
    
