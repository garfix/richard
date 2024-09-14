from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.Product import SomeProduct

@dataclass
class SimpleResponderProduct(SomeProduct):
    output: str


    def __str__(self) -> str:
        return self.output


    def log(self, logger: Logger):
        logger.add(str(self.output))


    def get_output(self) -> any:
        return self.output

