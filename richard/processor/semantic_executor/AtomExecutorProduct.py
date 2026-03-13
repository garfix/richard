from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.SomeProduct import SomeProduct

@dataclass
class AtomExecutorProduct(SomeProduct):
    bindings: list[dict]


    def log(self, logger: Logger):
            logger.add("\n".join(str(d) for d in self.bindings))


    def get_output(self) -> any:
        return self.bindings

