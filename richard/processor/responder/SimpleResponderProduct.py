from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.Product import Product

@dataclass
class SimpleResponderProduct(Product):
    output: str


    def __str__(self) -> str:
        return self.output


    def log(self, logger: Logger):
        logger.add(str(self.output))
