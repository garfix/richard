from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.Product import SomeProduct

@dataclass
class BasicTokenizerProduct(SomeProduct):
    tokens: list[str]


    def log(self, logger: Logger):
        logger.add("Tokens: " + ", ".join(self.tokens))


    def get_output(self) -> any:
        return self.tokens

