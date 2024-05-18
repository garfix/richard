from richard.entity.GrammarRules import GrammarRules
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeParser import SomeParser
from richard.interface.SomeTokenizer import SomeTokenizer
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.type.SimpleGrammar import SimpleGrammar
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
            

    def process(self, request: SentenceRequest) -> ProcessResult:
        tokens = self.tokenizer.get_tokens(request)
        return self.parser.parse(self.grammar, tokens)
    

    def get_tree(self, request: SentenceRequest) -> ParseTreeNode:
        return request.get_current_product(self)
    
