# TEST T

# ACTION (BUILD '#DKNOW-EPISODE)

# SUGGESTIONS
# (((GOALFORM GOAL PLANNER) (IS VAL PART) FOCUS-REQ)
# ((GOALFORM GOAL RECIPIENT) (IS VAL PART) FOCUS-REQ)
# ((GOALFORM GOAL FACT) (CON) FOCUS-REQ)
# ((ATTEMPTS) FIND-OUT-AT-REQ))

# MESSAGE (PRTGOAL (PATH '(GOALFORM GOAL) !STRUCT!))

# FOUNDER T

class Request:
    test: str # todo: condition
    action: str
    suggestions: list[str]
    message: str
    founder: str

