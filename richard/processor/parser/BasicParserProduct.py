from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.interface.SomeProduct import SomeProduct


@dataclass
class BasicParserProduct(SomeProduct):
    # one or parse trees derived from a single input
    # all of these trees together form a single ambiguous variant
    parse_trees: list[ParseTreeNode]


    def log(self, logger: Logger):
        for parse_tree in self.parse_trees:
            logger.add(str(parse_tree).strip())


    def get_output(self) -> any:
        return self.parse_trees
