from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.interface.Product import SomeProduct


@dataclass
class BasicParserProduct(SomeProduct):
    parse_tree: ParseTreeNode


    def log(self, logger: Logger):
        logger.add(str(self.parse_tree).strip())


    def get_output(self) -> any:
        return self.parse_tree
