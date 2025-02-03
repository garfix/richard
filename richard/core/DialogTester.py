from math import ceil
import unittest
import cProfile
import time

from richard.core.System import System
from richard.core.Logger import ALL, LAST, Logger
from richard.entity.SentenceRequest import SentenceRequest

class DialogTester:

    test_case: unittest.TestCase
    tests: list
    system: System

    # what to print? none, all, last
    logger: Logger

    # profile all tests and print the results
    profile: bool


    def __init__(self,
        test_case: unittest.TestCase,
        tests: list,
        system: System,
        logger: Logger,
        profile: bool = False
    ) -> None:
        self.test_case = test_case
        self.tests = tests
        self.system = system
        self.logger = logger
        self.profile = profile


    def run(self, ):
        if self.profile:
            cProfile.runctx('self.do_run()', globals(), locals(), None, 'cumulative')
        else:
            self.do_run()


    def do_run(self):
        last = self.tests[-1] if len(self.tests) > 0 else None
        for i, test in enumerate(self.tests):

            question, expected = test

            log_this = self.logger.which_tests == ALL or (self.logger.which_tests == LAST and test == last)
            self.logger.is_last_test = log_this

            request = SentenceRequest(question, logger=self.logger)
            try:
                if log_this:
                    self.logger.add_test_separator(i+1)
                    self.logger.add_key_value('Human', question)

                start_time = time.perf_counter()

                # send the request through the pipeline
                self.system.enter(request)

                end_time = time.perf_counter()

                output = ''
                if self.system.output_generator:
                    output = self.system.read_output()

                error = output != expected

                if log_this or error:
                    self.logger.add_key_value('Computer', output)
                    self.logger.add_comment(str(ceil((end_time - start_time) * 1000)) + " msecs")

                self.test_case.assertEqual(output, expected)

            except Exception as e:
                print(self.logger)
                raise e
