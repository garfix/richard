from math import ceil
import unittest
import cProfile
import time

from richard.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest

class Tester:

    test_case: unittest.TestCase
    pipeline: Pipeline
    tests: list

    # print anything if all is well
    print: bool

    # profile all tests and print the results
    profile: bool


    def __init__(self,
        test_case: unittest.TestCase, 
        pipeline: Pipeline, 
        tests: list,
        print: bool = True,
        profile: bool = False
    ) -> None:
        self.test_case = test_case
        self.pipeline = pipeline
        self.tests = tests
        self.print = print
        self.profile = profile


    def run(self, ):
        if self.profile:
            cProfile.runctx('self.do_run()', globals(), locals(), None, 'cumulative')
        else:
            self.do_run()


    def do_run(self):
        for test in self.tests:
            question, answer = test

            start_time = time.perf_counter()
            request = SentenceRequest(question)
            try:
                result = self.pipeline.enter(request)
                error = result != answer

                end_time = time.perf_counter()

                if self.print or error:
                    print("\n" + question)
                    print("> " + str(result))
                    print(str(ceil((end_time - start_time) * 1000)) + " msecs")

                if error:
                    self.pipeline.print_debug(request)

            except Exception as e:
                print("\n" + question)
                self.pipeline.print_debug(request)
                raise e

            self.test_case.assertEqual(answer, result)

