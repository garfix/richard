import unittest

from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestTokenizer(unittest.TestCase):
   
    def test_tokenizer(self):

        tokenizer = BasicTokenizer()

        tests = [
            { "input": "John walks home.", "expected": ["John", "walks", "home", "."]},
            { "input": "Did John's dog walk home?", "expected": ["Did", "John", "'", "s", "dog", "walk", "home", "?"]},
            { "input": "vacuum_cleaner, vacuum-cleaner", "expected": ["vacuum_cleaner", ",", "vacuum", "-", "cleaner"]},
        ]

        for test in tests:
            result = tokenizer.process(SentenceRequest(test["input"]))
            self.assertEqual(result.products[0], test["expected"])

    
