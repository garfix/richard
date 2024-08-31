NONE = 'none'
LAST = 'last'
ALL = 'all'

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
        self.entries.append(entry)


    def __str__(self) -> str:
        s = ""
        for entry in self.entries:
            s += str(entry) + "\n"
        return s


nullLogger = Logger()
nullLogger.log_no_tests()
