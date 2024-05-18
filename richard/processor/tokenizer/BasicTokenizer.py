import re
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeTokenizer import SomeTokenizer


class BasicTokenizer(SomeTokenizer):

    BASIC_TOKEN_RE = "([a-zA-Z_0-9]+|[^\\s])"
    
    token_expression: re.Pattern

    def __init__(self) -> None:
        super().__init__()
        self.token_expression = re.compile(self.BASIC_TOKEN_RE)

    def process(self, request: SentenceRequest) -> ProcessResult:
        tokens = self.token_expression.findall(request.text)
        return ProcessResult([tokens], "", [])


    def get_tokens(self, request: SentenceRequest) -> list[str]:
        return request.get_current_product(self)
