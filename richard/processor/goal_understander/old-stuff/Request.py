# FIND-OUT-REQ

# TEST T

# ACTION (BUILD '#DKNOW-EPISODE)

# SUGGESTIONS
# (((GOALFORM GOAL PLANNER) (IS VAL PART) FOCUS-REQ)
# ((GOALFORM GOAL RECIPIENT) (IS VAL PART) FOCUS-REQ)
# ((GOALFORM GOAL FACT) (CON) FOCUS-REQ)
# ((ATTEMPTS) FIND-OUT-AT-REQ))

# MESSAGE (PRTGOAL (PATH '(GOALFORM GOAL) !STRUCT!))

# FOUNDER T

from richard.processor.goal_understander.data.Suggestion import Suggestion


class Request:
    test: str # todo: condition
    action: str
    suggestions: list[Suggestion]
    message: str
    founder: str

    # suggestions should probably be a method
    def suggestions(self):
        pass
