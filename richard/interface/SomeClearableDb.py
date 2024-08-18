from abc import abstractmethod


class SomeClearableDb:
    @abstractmethod
    def clear(self):
        pass