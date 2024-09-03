import re
from richard.core.Logger import Logger
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.tokenizer.BasicTokenizerProduct import BasicTokenizerProduct


class BasicTokenizer(SomeProcessor):

    BASIC_TOKEN_RE = "([a-zA-Z_0-9]+|[^\\s])"

    token_expression: re.Pattern


    def __init__(self) -> None:
        super().__init__()
        self.token_expression = re.compile(self.BASIC_TOKEN_RE)


    def get_name(self) -> str:
        return "Tokenizer"


    def process(self, request: SentenceRequest) -> ProcessResult:
        tokens = self.token_expression.findall(request.text)
        product = BasicTokenizerProduct(tokens)
        return ProcessResult([product], "")


    def log_product(self, product: BasicTokenizerProduct, logger: Logger):
        logger.add("Tokens: " + ", ".join(product.tokens))
