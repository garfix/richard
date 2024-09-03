from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.interface.Product import Product


@dataclass
class BasicParserProduct(Product):
    parse_tree: ParseTreeNode


    def log(self, logger: Logger):
        logger.add(str(self.parse_tree).strip())