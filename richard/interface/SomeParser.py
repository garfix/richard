from abc import ABC, abstractmethod

from richard.entity.ProcessResult import ProcessResult
from richard.interface.SomeProcessor import SomeProcessor


class SomeParser(SomeProcessor):

    @abstractmethod
    def get_name(self) -> str:
        pass


    @abstractmethod
    def process(self, request) -> ProcessResult:
        pass

