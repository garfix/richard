from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor


class Multilingual:
    """
    This compositing processor takes other processors as input and uses the processor of the active language when asks to `process` input
    It can be used to combine any combinations of processors, like tokenization processors or parsing processors
    """
    
    processors: dict[str, Processor]
    language_switcher: Processor

    def __init__(self, processors: dict[str, Processor], language_switcher: Processor) -> None:
        super().__init__()
        self.processors = processors
        self.language_switcher = language_switcher

        
    def process(self, request: SentenceRequest):

        locale = request.get_current_product(self.language_switcher)

        if locale not in self.processors:
            raise Exception("No processor available for locale " + locale)

        return self.processors[locale].process(request)
    
