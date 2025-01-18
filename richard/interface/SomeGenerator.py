from abc import ABC, abstractmethod


class SomeGenerator(ABC):

    @abstractmethod
    def generate_output(self) -> str:
        pass
