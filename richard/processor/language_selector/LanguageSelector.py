from richard.core.Logger import Logger
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeLanguageSelector import SomeLanguageSelector


class LanguageSelector(SomeLanguageSelector):
    """
    Just picks one of the available locales, one by one. If processing the input with one locale fails, the next locale is tried.
    Always used in combination with the `Multilingual` composite processor.
    """

    locales: list[str]

    def __init__(self, locales: list[str]) -> None:
        super().__init__()
        self.locales = locales


    def get_name(self) -> str:
        return "Language selector"


    def process(self, request: SentenceRequest) -> ProcessResult:
        return ProcessResult(self.locales, "")


    def get_locale(self, request: SentenceRequest) -> str:
        return request.get_current_product(self)

    def log_product(self, product: any, logger: Logger):
        logger.add(", ".join(product))
