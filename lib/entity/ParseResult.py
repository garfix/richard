from dataclasses import dataclass

from lib.entity.ParseTreeNode import ParseTreeNode


@dataclass
class ParseResult:
    trees: list[ParseTreeNode]
    error: str
    error_arg: str

