from abc import ABC, abstractmethod


class SomeLogger(ABC):
    @abstractmethod
    def is_active(self):
        pass

    @abstractmethod
    def add_debug(self, code: str, text: str):
        pass
