from abc import abstractmethod
from richard.core.Logger import Logger


class SomeProduct:
    @abstractmethod
    def log(self, logger: Logger):
        pass


    @abstractmethod
    def get_output(self) -> any:
        """
        When this product is the output of the pipeline, this is its value
        """
        pass
