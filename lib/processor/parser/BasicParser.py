from lib.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from lib.entity.GrammarRules import GrammarRules
from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor
from lib.processor.parser.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from lib.type.SimpleGrammar import SimpleGrammar
from .EarleyParser import EarleyParser


class BasicParser(Processor):

    tokenizer: Processor
    grammar: GrammarRules
    parser: EarleyParser


    def __init__(self, grammar: SimpleGrammar, tokenizer: Processor) -> None:

        self.tokenizer = tokenizer

        sgrp = SimpleGrammarRulesParser()
        self.grammar = sgrp.parse(grammar)
        self.parser = EarleyParser()
            

    def process(self, request: SentenceRequest):
        tokens = request.get_current_product(self.tokenizer)
        result = self.parser.parse(self.grammar, tokens)
        return result.trees
    
