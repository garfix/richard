from richard.core.Logger import Logger
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.language_selector.LanguageSelectorProduct import LanguageSelectorProduct


class LanguageSelector(SomeProcessor):
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
        products = [LanguageSelectorProduct(locale) for locale in self.locales]
        return ProcessResult(products, "")


    def log_product(self, product: LanguageSelectorProduct, logger: Logger):
        logger.add(", ".join(product.locale))
