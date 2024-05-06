from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor


class LanguageSwitcher(Processor):

    locales: list[str]

    def __init__(self, locales: list[str]) -> None:
        super().__init__()
        self.locales = locales

    def process(self, request: SentenceRequest):
        return self.locales
    
