from abc import ABC, abstractmethod

from richard.store.Record import Record
from richard.store.RecordSet import RecordSet


class SomeDb(ABC):
    @abstractmethod
    def select(self) -> RecordSet:
        pass

    @abstractmethod
    def insert(self, record: Record):
        pass

    @abstractmethod
    def delete(self, record: Record):
        pass
