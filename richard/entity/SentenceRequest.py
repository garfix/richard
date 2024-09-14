from richard.core.Logger import ALL, Logger, nullLogger
from richard.entity.ProcessingException import ProcessingException
from richard.entity.ProcessResult import ProcessResult
from richard.interface.Product import SomeProduct
from richard.interface.SomeProcessor import SomeProcessor


class SentenceRequest:
    """
    A request is the data structure that keeps track of the active interpretation of the sentence.
    This interpretation consists of one alternative interpretation per processor so far.
    """

    # raw text that serves as the input to the request
    text: str

    # each processor creates one or more products; the pipeline considers these one by one; the current product is kept here
    current_products: dict[SomeProcessor, any]

    # all alternative products (more than one product suggests ambiguity)
    alternative_products: dict[SomeProcessor, list[any]]

    logger: Logger


    def __init__(self, text: str, logger: Logger = nullLogger) -> None:
        self.text = text
        self.current_products = {}
        self.alternative_products = {}
        self.logger = logger


    def set_alternative_products(self, processor: SomeProcessor, alternatives: list[any]):
        self.alternative_products[processor] = alternatives


    def get_alternative_products(self, processor: SomeProcessor) -> list[any]:
        if processor in self.alternative_products:
            return self.alternative_products[processor]
        else:
            return []


    def exec_process(self, processor: SomeProcessor) -> ProcessResult:
        try:
            result = processor.process(self)
        except ProcessingException as e:
            result = ProcessResult([], e.error)

        self.logger.add_process_result(processor, result)
        return result


    def set_current_product(self, processor: SomeProcessor, alternative: any):
        self.current_products[processor] = alternative


    def get_current_product(self, processor: SomeProcessor) -> SomeProduct|None:
        if processor in self.current_products:
            return self.current_products[processor]
        else:
            return None

