from lib.interface.Processor import Processor


class SentenceRequest:
    """
    A request is the data structure that keeps track of the active interpretation of the sentence.
    This interpretation consists of one alternative interpretation per processor so far.
    """

    # raw text that serves as the input to the request
    text: str

    # each processor creates one or more products; the pipeline considers these one by one; the current product is kept here
    current_products: dict[Processor, any] = {}

    # all alternative products (more than one product suggests ambiguity)
    alternative_products: dict[Processor, list[any]] = {}


    def __init__(self, text: str) -> None:
        self.text = text


    def set_alternative_products(self, processor: Processor, alternatives: list[any]):
        self.alternative_products[processor] = alternatives


    def get_alternative_products(self, processor: Processor) -> list[any]:
        return self.alternative_products[processor]


    def set_current_product(self, processor: Processor, alternative: any):
        self.current_products[processor] = alternative


    def get_current_product(self, processor: Processor):
        if processor in self.current_products:
            return self.current_products[processor]
        else:
            raise Exception("No product available for " + processor.__class__.__name__)
    