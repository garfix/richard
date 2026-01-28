import unittest

from tests.unit.micro_pam.MicroPAM import MicroPAM

class TestMicroPAM(unittest.TestCase):

    def test_micro_pam(self):

        init_rules = []
        sub_for = []
        plans_for = []
        instof = []
        inference_rules = []

        micro_pam = MicroPAM(init_rules, sub_for, plans_for, instof, inference_rules)

        story = [
            # Willa was hungry
            [],
            # She picked up the Michelin guide
            [],
            # She got into her car
            []
        ]

        for cd in story:
            micro_pam.justify(cd)
