import unittest

from tests.unit.micro_pam.MicroPAM import MicroPAM

class TestMicroPAM(unittest.TestCase):

    def test_micro_pam(self):

        # relate themes to goals
        init_rules = [
            [
                [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
                [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]]
            ],
        ]

        # relate goals to plans
        plans_for = [
            [
                [['goal', ['planner', '?x'], ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]]],
                [['take-plan', ['planner', '?x'], ['object', '?y']]]
            ],
            [
                [['goal', ['planner', '?x'],
                          ['objective', ['know', ['actor', '?x'],
                                                 ['fact', ['is', ['actor', 'restaurant'], ['prox', '?z']]]]]]]
                [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'restaurant-guide', '?w']]
            ],
            [
                [['goal', ['planner', '?x'], ['objective', ['enjoyment', ['actor', '?x']]]]],
                [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'book', '?w']]

            ],
            [
                [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]],
                [['do-$restaurant-plan', ['planner', '?x'], ['restaurant', '?y']]]

            ],
            [
                [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
                [['walk-plan', ['planner', '?x'], ['location', '?y']]]
            ],
            [
                [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
                [['use-vehicle-plan', ['planner', '?x']]]

            ],
        ]

        # preconditions of a plan
        sub_for = [
            [
                [['read-plan', ['planner', '?x'], ['object', '?y']]],
                [['goal', ['planner', '?x'],
                          ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]], ['isa', 'book', '?y']]
            ],
            [

            ],
            [

            ],
            [

            ],
        ]

        # possible instances of a plan
        instof = [
            [
                [['take-plan', ['planner', '?x'], ['object', '?y']]],
                [['grasp', ['actor', '?x'], ['object', '?y']]]
            ],
            [
                [['walk-plan', ['planner', '?x'], ['location', '?y']]],
                [['ptrans', ['actor', '?x'], ['object', '?x'], ['to', '?y']]]
            ]
        ]

        micro_pam = MicroPAM(init_rules, sub_for, plans_for, instof)

        story = [
            # Willa was hungry
            [
                ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]]
            ],
            # She picked up the Michelin guide
            [
                ['grasp', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]]
            ],
            # She got into her car
            [
                ['ptrans', ['actor', ['person', ['name', ['Willa']]]], ['object', ['person', ['name', ['Willa']]]], ['to', ['car']]]
            ]
        ]

        for cd in story:
            micro_pam.justify(cd)
