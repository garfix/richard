from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor


class LanguageSelector(Processor):
    """
    Just picks one of the available locales, one by one. If processing the input with one locale fails, the next locale is tried.
    Always used in combination with the `Multilingual` composite processor.
    """

    locales: list[str]
    
    def __init__(self, locales: list[str]) -> None:
        super().__init__()
        self.locales = locales

    def process(self, request: SentenceRequest):
        return self.locales
    
