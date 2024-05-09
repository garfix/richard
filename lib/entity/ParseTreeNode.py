from __future__ import annotations
from dataclasses import dataclass
from lib.entity.GrammarRule import GrammarRule


@dataclass(frozen=True)
class ParseTreeNode:

    category: str
    children: list[ParseTreeNode]
    form: str
    rule: GrammarRule
    sem: callable


    def is_leaf_node(self) -> bool:
        return len(self.children) == 0
    

    def __str__(self, indent: str = "    "):
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
    
    
    def child_sem(self, category: str = ""):
        """
        If category is "" it returns the semantics of this node.
        If not empty, it returns the sem of the child with named category.
        Use "/" to access a deeper child.
        """
        if category == "":
            return self.rule.sem

        node = self
        for step in category.split("/"):
            found = False
            for child in node.children:
                if child.category == step:
                    node = child
                    found = True
            if not found:
                raise Exception("No child node " + step + " found for " + node.category)
        return node.rule.sem
    

    def child(self, category: str = ""):
        """
        If category is "" it returns the semantics of this node.
        If not empty, it returns the sem of the child with named category.
        Use "/" to access a deeper child.
        """
        if category == "":
            return self.rule.sem

        node = self
        for step in category.split("/"):
            found = False
            for child in node.children:
                if child.category == step:
                    node = child
                    found = True
            if not found:
                raise Exception("No child node " + step + " found for " + node.category)
        return node
