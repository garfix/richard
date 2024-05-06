from lib.interface.Processor import Processor


class SentenceRequest:
    """
    A request is the data structure that keeps track of the active interpretation of the sentence.
    This interpretation consists of one alternative interpretation per processor so far.
    """

    text: str
    # an alternative may be a parse tree, an intent, or something else
    alternatives: dict[Processor, any] = {}


    def __init__(self, text: str) -> None:
        self.text = text


    def set_current_product(self, processor: Processor, alternative: any):
        self.alternatives[processor] = alternative


    def get_current_product(self, processor: Processor):
        if processor in self.alternatives:
            return self.alternatives[processor]
        else:
            raise Exception("No alternative available for this processor")
    