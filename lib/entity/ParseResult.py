from dataclasses import dataclass

from lib.entity.ParseTreeNode import ParseTreeNode


@dataclass
class ParseResult:
    root_nodes: list[ParseTreeNode]
    error: str
    error_arg: str

