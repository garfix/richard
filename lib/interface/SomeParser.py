from abc import abstractmethod

from lib.entity.ParseTreeNode import ParseTreeNode
from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.SomeProcessor import SomeProcessor


"""
Every processor needs to have access to the current alternative interpretation of its predecessor.
To this end it must inject these processors as dependencies. The dependency serves as a key: 
    only with the key can the pipeline be sure that the dependent processor exists.
"""
class SomeParser(SomeProcessor):
    @abstractmethod
    def get_tree(self, request: SentenceRequest) -> ParseTreeNode: 
        pass
