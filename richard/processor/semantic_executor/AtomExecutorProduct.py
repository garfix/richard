from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.Product import Product

@dataclass
class AtomExecutorProduct(Product):
    bindings: list[dict]
    stats: dict[str, int]


    def log(self, logger: Logger):
            logger.add("\n".join(str(d) for d in self.bindings))

            if self.stats:
                 logger.add_subheader("Stats")
                 logger.add("\n".join("{}: {}".format(predicate, count) for predicate, count in self.stats.items()))
