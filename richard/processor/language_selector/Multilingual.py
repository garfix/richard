from richard.core.Logger import Logger
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.language_selector.LanguageSelectorProduct import LanguageSelectorProduct


class Multilingual(SomeProcessor):
    """
    This compositing processor takes other processors as input and uses the processor of the active language when asks to `process` input
    It can be used to combine any combinations of processors, like parsing processors
    """

    processors: dict[str, SomeProcessor]
    language_selector: SomeProcessor

    def __init__(self, processors: dict[str, SomeProcessor], language_selector: SomeProcessor) -> None:
        super().__init__()
        self.processors = processors
        self.language_selector = language_selector


    def get_name(self) -> str:
        return "Multilingual Language selector"


    def process(self, request: SentenceRequest) -> ProcessResult:

        incoming: LanguageSelectorProduct = request.get_current_product(self.language_selector)

        if incoming.locale not in self.processors:
            raise Exception("No processor available for locale " + incoming.locale)

        return self.processors[incoming.locale].process(request)


    def log_product(self, product: any, logger: Logger):
        logger.add(str(product))
