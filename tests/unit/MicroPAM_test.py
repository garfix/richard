import unittest

from pprint import pprint
from tests.unit.micro_pam.MicroPAM import MicroPAM
from tests.unit.micro_pam.cd_functions import instantiate, match

class TestMicroPAM(unittest.TestCase):

    def test_match(self):
        result = match(['person', '?x'], ['person', ['name', 'John']], {'y': 2})
        self.assertEqual(result, {'x': ['name', 'John'], 'y': 2})

        result = match(['person', '?x'], ['person', ['name', 'John']], {'x': ['name', 'John']})
        self.assertEqual(result, {'x': ['name', 'John']})

        result = match(['person', '?x'], ['person', ['name', 'John']], {'x': ['name', 'Jackie']})
        self.assertEqual(result, None)

        result = match(['person', '?x'], ['person', ['name', 'John']], {'x': 2})
        self.assertEqual(result, None)

        result = match([['person', '?x']], [['person', ['name', 'John']]], {})
        self.assertEqual(result, {'x': ['name', 'John']})

        result = match([['person', '?x']], [['person', ['name', 'John']], ['profession', 'baker']], {})
        self.assertEqual(result, {'x': ['name', 'John']})

        pattern = ['ptrans', ['actor', '?shopper'], ['object', '?shopper'], ['to', '?store']]
        cd = ['ptrans', ['actor', ['person', ['name', ['Jack']]]], ['object', ['person', ['name', ['Jack']]]], ['to', ['store']]]
        result = match(pattern, cd, {})
        self.assertEqual(result, {'shopper': ['person', ['name', ['Jack']]], 'store': ['store']})


    def test_instantiate(self):
        result = instantiate(['person', ['name', '?x']], {'x': 'John'})
        self.assertEqual(result, ['person', ['name', 'John']])


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
                                                 ['fact', ['is', ['actor', 'restaurant'], ['prox', '?z']]]]]]],
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
            # to be close to a location, know the proximity of the actor to the location
            [
                [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
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
        instance_of = [
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

        micro_pam = MicroPAM(init_rules, sub_for, plans_for, instance_of)

        story = [
            # Willa was hungry
            ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],
            # She picked up the Michelin guide
            ['grasp', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
            # She got into her car
            ['ptrans', ['actor', ['person', ['name', ['Willa']]]], ['object', ['person', ['name', ['Willa']]]], ['to', ['car']]]
        ]

        expected_logs = [
            [
                "Trying to explain",
                ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],
                "Does not confirm prediction",
                "No usable inferences from",
                ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],
                # - does not fire any inferences
                "No inference chain found - adding",
                ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],
                "---theme"
            ],
            [
                "Trying to explain",
                ['grasp', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
                "Does not confirm prediction",
                # - inference: grasp instance_of take-plan (grasp action is an instance of the take-plan)
                "Possible explanation assuming",
                ['take-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
                "Does not confirm prediction",
                # - inference: take-plan plans_for goal (take-plan is used for the possession goal)
                "Possible explanation assuming",
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['poss', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]]]],
                "Does not confirm prediction",
                # - inference: goal sub_for read-plan (possession goal is a sub-goal of the read-plan)
                "Possible explanation assuming",
                ['read-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
                "Does not confirm prediction",
                # - inference: read-plan plans_for enjoyment (read-plan is used for the enjoyment goal)
                "Possible explanation assuming",
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['enjoyment', ['actor', ['person', ['name', ['Willa']]]]]]],
                "Does not confirm prediction",
                # - no further inferences
                "No usable inferences from",
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['enjoyment', ['actor', ['person', ['name', ['Willa']]]]]]],
                # - inference: read-plan plans_for goal (read-plan is used for knowing a fact)
                "Possible explanation assuming",
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['know', ['actor', ['person', ['name', ['Willa']]]], ['fact', ['is', ['actor', 'restaurant'], ['prox', None]]]]]],
                "Does not confirm prediction",
                # - inference: goal sub_for goal (goal know proximity is used as a sub-goal for be in proximity)
                "Possible explanation assuming",
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['prox', ['actor', ['person', ['name', ['Willa']]]], ['location', 'restaurant']]]],
                "Does not confirm prediction",
                # - inference: goal to be in proximity of a restaurant is used as a sub-goal of the do-$restaurant-plan
                "Possible explanation assuming",
                ['do-$restaurant-plan', ['planner', ['person', ['name', ['Willa']]]], ['restaurant', 'restaurant']],
                "Does not confirm prediction",
                # - inference goal do-$restaurant-plan plans_for goal to not be hungry
                "Possible explanation assuming",
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [0]]]]]]],
                # - this event was predicted, as it matches the contents of the first line of the story
                "Confirms prediction from",
                ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],
                # - adding inferences to database
                "Adding inference chain to data base",
                ['do-$restaurant-plan', ['planner', ['person', ['name', ['Willa']]]], ['restaurant', 'restaurant']],
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['prox', ['actor', ['person', ['name', ['Willa']]]], ['location', 'restaurant']]]],
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['know', ['actor', ['person', ['name', ['Willa']]]], ['fact', ['is', ['actor', 'restaurant'], ['prox', None]]]]]],
                ['read-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['poss', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]]]],
                ['take-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
                ['grasp', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
                ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [0]]]]]]],
            ],
            [
                "Trying to explain",
            ]
        ]

        for cd, expected_log in zip(story, expected_logs):
            log = []

            print(f"Story line: {cd}")

            micro_pam.justify(cd, log)

            error = False
            if (len(log) != len(expected_log)):
                print(f"Expected lines: {len(expected_log)}, got: {len(log)}")
                error = True
            else:
                for log_line, expected_log_line in zip(log, expected_log):
                    if (log_line != expected_log_line):
                        print(f"{log_line} != {expected_log_line}")
                        error = True

            if error:
                print("Expected:")
                print_log(expected_log)
                print()
                print("Received:")
                print_log(log)
                break



def print_log(log: list[str]):
    for line in log:
        if isinstance(line, list):
            print(f"    {line}")
        else:
            print(line)

