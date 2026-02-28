
                # [['take-plan', ['planner', '?x'], ['object', '?y']]],
                # [['grasp', ['actor', '?x'], ['object', '?y']]]

# grasp(E1, E2) => take_plan(E1, E2).
pick_up(E1, E2) => take_plan(E1, E2).
