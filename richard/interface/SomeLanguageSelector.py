from abc import abstractmethod

from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor


class SomeLanguageSelector(SomeProcessor):
    @abstractmethod
    def get_locale(self, request: SentenceRequest) -> str: 
        pass
