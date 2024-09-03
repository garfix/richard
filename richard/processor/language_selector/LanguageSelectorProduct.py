from dataclasses import dataclass

from richard.core.Logger import Logger
from richard.interface.Product import Product


@dataclass
class LanguageSelectorProduct(Product):
    locale: str


    def log(self, logger: Logger):
        logger.add(", ".join(self.locale))
