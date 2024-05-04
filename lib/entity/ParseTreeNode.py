from dataclasses import dataclass
from lib.entity.GrammarRule import GrammarRule


@dataclass()
class ParseTreeNode:
    category: str
    children: list
    form: str
    rule: GrammarRule

    def IsLeafNode(self) -> bool:
        return len(self.children) == 0
    

    # def to_string(self):
    #     return self.category + "/" + self.


    def IndentedString(self, indent):

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
            body += child.IndentedString(newIndent)

        return body
