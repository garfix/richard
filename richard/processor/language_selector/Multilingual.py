from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeLanguageSelector import SomeLanguageSelector
from richard.interface.SomeProcessor import SomeProcessor


class Multilingual(SomeProcessor):
    """
    This compositing processor takes other processors as input and uses the processor of the active language when asks to `process` input
    It can be used to combine any combinations of processors, like tokenization processors or parsing processors
    """
    
    processors: dict[str, SomeProcessor]
    language_selector: SomeLanguageSelector

    def __init__(self, processors: dict[str, SomeProcessor], language_selector: SomeLanguageSelector) -> None:
        super().__init__()
        self.processors = processors
        self.language_selector = language_selector

        
    def process(self, request: SentenceRequest) -> ProcessResult:

        locale = self.language_selector.get_locale(request)

        if locale not in self.processors:
            raise Exception("No processor available for locale " + locale)

        return self.processors[locale].process(request)
    

    def get_product(self, request: SentenceRequest) -> any:
        return request.get_current_product(self)
    
