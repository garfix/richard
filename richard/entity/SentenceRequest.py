class SentenceRequest:

    # raw text that serves as the input to the request
    text: str

    def __init__(self, text: str) -> None:
        self.text = text

