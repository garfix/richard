from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.Product import Product

@dataclass
class BasicTokenizerProduct(Product):
    tokens: list[str]


    def log(self, logger: Logger):
        logger.add("Tokens: " + ", ".join(self.tokens))
