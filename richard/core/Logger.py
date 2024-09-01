from richard.entity.ProcessResult import ProcessResult
from richard.interface.SomeProcessor import SomeProcessor


NONE = 'none'
LAST = 'last'
ALL = 'all'

NO_COLOR = '\033[0m'
HEADER_COLOR = '\033[33m'
SUBHEADER_COLOR = '\033[96m'
VALUE_COLOR = '\033[37m'
SEPARATOR_COLOR = '\033[32m'
KEY_COLOR = '\033[34m'
ERROR_COLOR = '\033[31m'

class Logger:

    which_tests: str
    show_alternatives: str
    show_processors: list

    is_last_test: bool

    show_active: bool

    entries: list


    def __init__(self):
        self.which_tests = LAST
        self.is_last_test = False
        self.show_alternatives = NONE
        self.show_processors = []
        self.show_active = False
        self.entries = []


    def log_all_tests(self):
        """ Create logs for all tests """
        self.which_tests = ALL

    def log_only_last_test(self):
        """ Create logs only for the last test in the suite """
        self.which_tests = LAST

    def log_no_tests(self):
        """ Create no log for any test """
        self.which_tests = NONE


    def log_all_alternatives(self, *processors):
        """
        Create a log entry for all alternative products of a processor (for instance: all parse trees)
        processors: the products of these processors are logged (default = all)
        """
        self.show_alternatives = ALL
        self.show_processors = processors


    def log_active_products(self, *processors):
        """
        Create a log entry for each product when it is processed in a block
        processors: the products of these processors are logged (default = all)
        """
        self.show_active = True
        self.show_processors = processors


    def is_active(self):
        return (self.which_tests == ALL) or (self.which_tests == LAST and self.is_last_test)


    def add(self, entry):
        self.entries.append(entry + "\n")

    def add_test_separator(self, test_number: int):
         self.entries.append("\n{}~~[{} {} {}]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}\n"
            .format(SEPARATOR_COLOR, VALUE_COLOR, test_number, SEPARATOR_COLOR, NO_COLOR))


    def add_key_value(self, key: str, value: str):
        self.entries.append(("{}{}{}: {}\n").format(KEY_COLOR, key, NO_COLOR, value))


    def add_header(self, header):
        self.entries.append(HEADER_COLOR + header + NO_COLOR + "\n")


    def add_subheader(self, subheader):
        self.entries.append(SUBHEADER_COLOR + subheader + NO_COLOR + "\n")


    def add_error(self, error):
        self.entries.append(ERROR_COLOR + error + NO_COLOR + "\n")


    def add_process_result(self, processor: SomeProcessor, result: ProcessResult):
        if self.is_active() and self.show_alternatives == ALL:
            if not self.show_processors or processor in self.show_processors:
                self.add_header(processor.get_name())
                if result.error != "":
                    self.add_error(result.error)

                for product in result.products:
                    processor.log_product(product, self)


    def add_active_product(self, processor: SomeProcessor, alternative: any):
        if self.is_active() and self.show_active:
            if not self.show_processors or processor in self.show_processors:
                self.add_header(processor.get_name())
                processor.log_product(alternative, self)


    def __str__(self) -> str:
        s = ""
        for entry in self.entries:
            s += str(entry) + "\n"
        return s


nullLogger = Logger()
nullLogger.log_no_tests()
