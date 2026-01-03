import re
from richard.entity.GrammarRules import GrammarRules
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeParseTreeSortHeuristics import SomeParseTreeSortHeuristics
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.parser.helper.sentence_extractor import extract_sentences
from .tree_sort_heuristics.BasicParseTreeSortHeuristics import BasicParseTreeSortHeuristics
from .earley.EarleyParser import EarleyParser


class BasicParser(SomeProcessor):

    grammar: GrammarRules
    parser: EarleyParser
    tree_sorter: SomeParseTreeSortHeuristics
    sentence_categories: str


    def __init__(self, grammar: GrammarRules, sentence_categories = ["s"]) -> None:
        self.grammar = grammar
        self.parser = EarleyParser()
        self.tree_sorter = BasicParseTreeSortHeuristics()
        self.sentence_categories = sentence_categories


    def get_name(self) -> str:
        return "Parser"


    def process(self, request: SentenceRequest) -> ProcessResult:
        # replace whitespace sequences by single space
        source_text = re.sub('\s+', ' ', request.text)

        result = self.parser.parse(self.grammar, source_text)

        sorted_trees = self.tree_sorter.sort_trees(result.products)

        products = []
        for tree in sorted_trees:
            sentence_trees = extract_sentences(tree, self.sentence_categories)
            if len(sentence_trees) > 0:
                products.append(BasicParserProduct(sentence_trees))

        return ProcessResult(
            products,
            result.error_type,
            result.error_args
        )
