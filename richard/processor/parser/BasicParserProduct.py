from dataclasses import dataclass

from richard.entity.ParseTreeNode import ParseTreeNode


@dataclass
class BasicParserProduct:
    parse_tree: ParseTreeNode

