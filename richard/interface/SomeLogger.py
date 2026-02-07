from abc import ABC, abstractmethod

from richard.entity.ProcessResult import ProcessResult
from richard.interface.SomeProcessor import SomeProcessor


NONE = 'none'
LAST = 'last'
ALL = 'all'

class SomeLogger(ABC):

    which_tests: str
    is_last_test: bool
    show_stats: bool
    entries: list
    show_products: str

    @abstractmethod
    def is_active(self):
        pass

    @abstractmethod
    def log_all_tests(self):
        pass

    @abstractmethod
    def log_only_last_test(self):
        pass

    @abstractmethod
    def log_no_tests(self):
        pass

    @abstractmethod
    def log_products(self, *processors):
        pass

    @abstractmethod
    def add_test_separator(self, test_number: int):
        pass

    @abstractmethod
    def add_key_value(self, key: str, value: str):
        pass

    @abstractmethod
    def add_header(self, header):
        pass


    @abstractmethod
    def add_subheader(self, subheader):
        pass


    @abstractmethod
    def add_comment(self, comment):
        pass


    @abstractmethod
    def add_error(self, error):
        pass

    @abstractmethod
    def add_process_result(self, processor: SomeProcessor, result: ProcessResult):
        pass