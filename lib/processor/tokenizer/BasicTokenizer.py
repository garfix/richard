from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor


class BasicTokenizer(Processor):
    def process(self, request: SentenceRequest):
        tokens = request.text.split(" ")
        return [tokens]
