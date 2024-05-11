from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.SomeTokenizer import SomeTokenizer


class BasicTokenizer(SomeTokenizer):

    def process(self, request: SentenceRequest):
        tokens = request.text.split(" ")
        return [tokens]


    def get_tokens(self, request: SentenceRequest) -> list[str]:
        return request.get_current_product(self)
