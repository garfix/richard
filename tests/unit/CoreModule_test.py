import unittest

from richard.core.System import System
from richard.block.FindAll import FindAll
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.module.CoreModule import CoreModule
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer


class TestCoreModule(unittest.TestCase):

    def test_equals(self):

        core_module = CoreModule()
        bindings = core_module.equals([3, 5], None)
        self.assertEqual(bindings, [])

        bindings = core_module.equals([3, 3], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = core_module.equals([3, None], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = core_module.equals([None, 3], None)
        self.assertEqual(bindings, [[3, 3]])


    def test_deconstruct(self):
        pass
