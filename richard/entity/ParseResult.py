from dataclasses import dataclass

from richard.entity.ParseTreeNode import ParseTreeNode


@dataclass
class ParseResult:
    trees: list[ParseTreeNode]
    error: str
    error_arg: str

