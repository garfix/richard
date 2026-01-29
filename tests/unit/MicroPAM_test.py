import unittest

from tests.unit.micro_pam.MicroPAM import MicroPAM

class TestMicroPAM(unittest.TestCase):

    def test_micro_pam(self):

        # relate themes to goals
        init_rules = [
            # theme: to be in a fed state; goal: to not be hungry
            [
                [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
                [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]]
            ],
        ]

        # relate goals to plans
        plans_for = [
            # to possess an object, take the object
            [
                [['goal', ['planner', '?x'], ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]]],
                [['take-plan', ['planner', '?x'], ['object', '?y']]]
            ],
            # to know the distance to a restaurant, read a restaurant guide
            [
                [['goal', ['planner', '?x'],
                          ['objective', ['know', ['actor', '?x'],
                                                 ['fact', ['is', ['actor', 'restaurant'], ['prox', '?z']]]]]]]
                [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'restaurant-guide', '?w']]
            ],
            # to enjoy oneself, read a book
            [
                [['goal', ['planner', '?x'], ['objective', ['enjoyment', ['actor', '?x']]]]],
                [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'book', '?w']]

            ],
            # to not be hungry, go to a restaurant
            [
                [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]],
                [['do-$restaurant-plan', ['planner', '?x'], ['restaurant', '?y']]]

            ],
            # to be near a location, walk there
            [
                [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
                [['walk-plan', ['planner', '?x'], ['location', '?y']]]
            ],
            # to be near a location, use a vehicle
            [
                [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
                [['use-vehicle-plan', ['planner', '?x']]]

            ],
        ]

        # preconditions of a plan
        sub_for = [
            # to read, possess a book
            [
                [['read-plan', ['planner', '?x'], ['object', '?y']]],
                [['goal', ['planner', '?x'],
                          ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]], ['isa', 'book', '?y']]
            ],
            # to be close to a location, know ...(?)
            [
                [['goal', ['planner', '?x'], ['objective', ['prox', ['actor' '?x'], ['location', '?y']]]]],
                [['goal', ['planner', '?x'],
                          ['objective', ['know', ['actor', '?x'], ['fact', ['is', ['actor', '?y'], ['prox', '?z']]]]]]]
            ],
            # to visit a restaurant, be close to a restaurant
            [
                [['do-$restaurant-plan', ['planner', '?x'], ['restaurant', '?y']]],
                [['goal', ['planner', '?x'],
                          ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]], ['isa', 'restaurant', '?y']]
            ],
            # to use a vehicle, be close to a car
            [
                [['use-vehicle-plan', ['planner', '?x'], ['object', '?y']]],
                [['goal', ['planner', '?x'],
                          ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]], ['isa', 'car', '?y']]
            ],
        ]

        # possible instances of a plan
        instof = [
            # to take an object, means to grasp it
            [
                [['take-plan', ['planner', '?x'], ['object', '?y']]],
                [['grasp', ['actor', '?x'], ['object', '?y']]]
            ],
            # to walk to a location, means to physically transfer yourself to it
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
