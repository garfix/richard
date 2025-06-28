from __future__ import annotations
from dataclasses import dataclass
from richard.core.constants import POS_TYPE_REG_EXP
from richard.entity.GrammarRule import GrammarRule


@dataclass(frozen=True)
class ParseTreeNode:

    category: str
    children: list[ParseTreeNode]
    form: str
    rule: GrammarRule
    # the number of regular expression nodes below and including this node
    # including it here is a speed measure
    reg_exp_count: int

    def is_leaf_node(self) -> bool:
        return len(self.children) == 0


    def __str__(self, indent: str = ""):
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
            body += child.__str__(newIndent)

        return body

    def inline_str(self):
        body = ""
        sep = ""
        for i, child in enumerate(self.children):
            if child.form == " ":
                pass
            elif child.form != "":
                body += sep
                body += child.category + " '" + child.form + "'"
            else:
                body += sep
                body += child.inline_str()
            sep = " "

        return self.category + "(" + body + ")"
