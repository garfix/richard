from lib.entity.GrammarRules import GrammarRules
from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor
from lib.processor.language_switcher.LanguageSwitcher import LanguageSwitcher
from lib.processor.parser.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from lib.type.SimpleGrammar import SimpleGrammar
from .EarleyParser import EarleyParser


class MultiLingualParser(Processor):

    language_switcher: LanguageSwitcher
    tokenizer: Processor
    grammars: dict[str, GrammarRules]
    parser: EarleyParser


    def __init__(self, grammars: dict[str, SimpleGrammar], language_switcher: LanguageSwitcher, tokenizer: Processor) -> None:

        self.language_switcher = language_switcher
        self.tokenizer = tokenizer

        sgrp = SimpleGrammarRulesParser()

        self.grammars = { locale:sgrp.parse(rules) for (locale, rules) in grammars.items() }
        self.parser = EarleyParser()
            

    def process(self, request: SentenceRequest):
        locale = request.get_current_product(self.language_switcher)
        tokens = request.get_current_product(self.tokenizer)

        if locale not in self.grammars:
            raise Exception("No grammar available for locale " + locale)

        result = self.parser.parse(self.grammars[locale], tokens)
        return result.trees
    
