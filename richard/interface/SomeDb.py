from abc import ABC, abstractmethod

from richard.entity.Record import Record
from richard.entity.RecordSet import RecordSet


class SomeDb(ABC):
    @abstractmethod
    def select(self) -> RecordSet:
        pass

    @abstractmethod
    def assert_record(self, record: Record):
        pass

    @abstractmethod
    def retract_record(self, record: Record):
        pass
