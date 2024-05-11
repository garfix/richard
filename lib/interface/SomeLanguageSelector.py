from abc import abstractmethod

from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.SomeProcessor import SomeProcessor


class SomeLanguageSelector(SomeProcessor):
    @abstractmethod
    def get_locale(self, request: SentenceRequest) -> str: 
        pass
