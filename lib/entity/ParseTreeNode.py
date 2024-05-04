from __future__ import annotations
from dataclasses import dataclass
from lib.entity.GrammarRule import GrammarRule


@dataclass(frozen=True)
class ParseTreeNode:

    category: str
    children: list[ParseTreeNode]
    form: str
    rule: GrammarRule


    def is_leaf_node(self) -> bool:
        return len(self.children) == 0
    

    def indented_string(self, indent: str):
        body = ""

        if indent == "":
            body = self.category + "\n"

        for i, child in enumerate(self.children):
            if child.form != "":
                body += indent + "+- " + child.category + " '" + child.form + "'\n"
                continue

            body += indent + "+- " + child.category + "\n"
            newIndent = indent
            if i < len(self.children)-1:
                newIndent += "|  "
            else:
                newIndent += "   "
            body += child.indented_string(newIndent)

        return body
