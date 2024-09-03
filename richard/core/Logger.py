from richard.entity.ProcessResult import ProcessResult
from richard.interface.SomeProcessor import SomeProcessor
import shutil



NONE = 'none'
LAST = 'last'
ALL = 'all'

NO_COLOR = '\033[0m'
HEADER_COLOR = '\033[33m'
SUBHEADER_COLOR = '\033[36m'
VALUE_COLOR = '\033[37m'
SEPARATOR_COLOR = '\033[33m'
KEY_COLOR = '\033[34m'
ERROR_COLOR = '\033[31m'
COMMENT_COLOR = '\033[90m'

class Logger:

    which_tests: str

    show_products: str
    show_products_processors: list

    is_last_test: bool

    show_stats: bool
    show_stats_processors: bool

    entries: list


    def __init__(self):
        self.which_tests = LAST
        self.is_last_test = False
        self.show_products = NONE
        self.show_products_processors = []
        self.show_stats = False
        self.show_stats_processors = []
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


    def log_products(self, *processors):
        """
        Create a log entry for all alternative products of a processor (for instance: all parse trees)
        processors: the products of these processors are logged (default = all)
        """
        self.show_products = ALL
        self.show_products_processors = processors


    def log_stats(self, *processors):
        """
        Log statistics that some processors provide
        processors: the products of these processors are logged (default = all)
        """
        self.show_stats = True
        self.show_stats_processors = processors


    def is_active(self):
        """
        Should the current test be logged?
        """
        return (self.which_tests == ALL) or (self.which_tests == LAST and self.is_last_test)


    def add(self, entry):
        self.entries.append(entry + "\n")


    def add_test_separator(self, test_number: int):
        terminal_width = shutil.get_terminal_size().columns
        sep = "~" * terminal_width
        line = "{}~~[{} {} {}]{}".format(SEPARATOR_COLOR, VALUE_COLOR, test_number, SEPARATOR_COLOR, sep)
        truncated = line[:terminal_width + len(SEPARATOR_COLOR) + len(VALUE_COLOR) + len(SEPARATOR_COLOR)]
        self.entries.append(truncated + NO_COLOR + "\n")


    def add_key_value(self, key: str, value: str):
        self.entries.append(("{}[{}]{} {}\n").format(KEY_COLOR, key, NO_COLOR, value))


    def add_header(self, header):
        self.entries.append(HEADER_COLOR + header + NO_COLOR + "\n")


    def add_subheader(self, subheader):
        self.entries.append(SUBHEADER_COLOR + subheader + NO_COLOR + "\n")


    def add_comment(self, comment):
        self.entries.append(COMMENT_COLOR + comment + NO_COLOR + "\n")


    def add_error(self, error):
        self.entries.append(ERROR_COLOR + error + NO_COLOR + "\n")


    def add_process_result(self, processor: SomeProcessor, result: ProcessResult):
        if self.is_active() and self.show_products == ALL:
            if not self.show_products_processors or processor in self.show_products_processors:
                self.add_header(processor.get_name())
                if result.error != "":
                    self.add_error(result.error)

                for product in result.products:
                    product.log(self)


    def add_active_product(self, processor: SomeProcessor, alternative: any):
        if self.is_active() and self.show_active:
            if not self.show_products_processors or processor in self.show_products_processors:
                self.add_header(processor.get_name())
                alternative.log(self)


    def should_log_stats(self, processor: SomeProcessor):
        if self.is_active() and self.show_stats:
            if not self.show_stats_processors or processor in self.show_stats_processors:
                return True
        return False


    def __str__(self) -> str:
        s = ""
        for entry in self.entries:
            s += str(entry) + "\n"
        return s


nullLogger = Logger()
nullLogger.log_no_tests()
