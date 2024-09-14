from dataclasses import dataclass

from richard.core.Logger import Logger
from richard.interface.Product import SomeProduct


@dataclass
class LanguageSelectorProduct(SomeProduct):
    locale: str


    def log(self, logger: Logger):
        logger.add(", ".join(self.locale))


    def get_output(self) -> any:
        return self.locale
