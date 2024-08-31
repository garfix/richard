from math import ceil
import unittest
import cProfile
import time

from richard.core.Pipeline import Pipeline
from richard.entity.Logger import ALL, LAST, Logger
from richard.entity.SentenceRequest import SentenceRequest

class DialogTester:

    test_case: unittest.TestCase
    pipeline: Pipeline
    tests: list

    # what to print? none, all, last
    logger: Logger

    # profile all tests and print the results
    profile: bool


    def __init__(self,
        test_case: unittest.TestCase,
        pipeline: Pipeline,
        tests: list,
        logger: Logger,
        profile: bool = False
    ) -> None:
        self.test_case = test_case
        self.pipeline = pipeline
        self.tests = tests
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

            question, answer = test

            log_this = self.logger.which_tests == ALL or (self.logger.which_tests == LAST and test == last)
            self.logger.is_last_test = log_this

            request = SentenceRequest(question, logger=self.logger)
            try:
                if log_this:
                    self.logger.add("\n~~ [ {} ] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(i + 1))
                    self.logger.add("\n" + question + "\n")

                start_time = time.perf_counter()
                result = self.pipeline.enter(request)
                end_time = time.perf_counter()

                error = result != answer

                if log_this or error:
                    self.logger.add("\n> " + str(result))
                    self.logger.add(str(ceil((end_time - start_time) * 1000)) + " msecs")

                self.test_case.assertEqual(answer, result)

            except Exception as e:
                print(self.logger)
                raise e
