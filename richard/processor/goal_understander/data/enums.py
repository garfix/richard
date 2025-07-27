from enum import Enum


class Action(Enum):
    INGEST = "ingest"        # Eat or drink
    EXPEL = "expel"          # Eliminate waste
    MOVE = "move"            # Change location
    MTRANS = "mtrans"        # Mental transfer (communicate, believe)
    ATRANS = "atrans"        # Abstract transfer (ownership)
    PTRANS = "ptrans"        # Physical transfer (give, take)
    PROPEL = "propel"        # Cause movement
    GRASP = "grasp"          # Grabbing or taking
    BUILD = "build"          # Construct, make
    DESTROY = "destroy"      # Eliminate or ruin
    ATTEND = "attend"        # Perceive or look at
    DLINK = "dlink"          # Dislike
    PLINK = "plink"          # Like
    EVAL = "eval"            # Evaluate or judge
    DKNOW = "dknow"          # Don't know (Delta know?)

class CaseRole(Enum):
    ACTOR = "actor"              # Who performs the action
    OBJECT = "object"            # What the action is performed on
    INSTRUMENT = "instrument"    # What is used to perform the action
    FROM = "from"                # Source of movement or transfer
    TO = "to"                    # Destination of movement or transfer
    MOD = "mod"                  # Manner or adverbial modification
    TIME = "time"                # When the action occurs
    PLACE = "place"              # Where the action occurs
    MOTIVATION = "motivation"    # Why the action is done
    RESULT = "result"            # The outcome of the action
    BENEFICIARY = "beneficiary"  # Who benefits from the action
    EXPERIENCER = "experiencer"  # Who experiences an emotion or perception
    RECIPIENT = "recipient"      # Who receives something (esp. in MTRANS, ATRANS)
    GOAL = "goal"                # The desired end-state
    SOURCE = "source"            # Where the object originally comes from

class MemoryTag(Enum):
    EPISODE = "episode"           # A specific remembered event
    EXPERIENCE = "experience"     # A lived or perceived situation
    SCRIPT = "script"             # A stereotypical, generalized event sequence
    GOAL = "goal"                 # A remembered goal or intention
    PLAN = "plan"                 # A strategy to achieve a goal
    FACT = "fact"                 # A known (static) fact
    BELIEF = "belief"             # A held belief (may be subjective)
    EXPECTATION = "expectation"   # Anticipated event or result
    INTENTION = "intention"       # A future-directed goal
    PROBLEM = "problem"           # A recognized problem state
    SOLUTION = "solution"         # A remembered solution
    FAILURE = "failure"           # A goal that failed
    DKNOW = "dknow"               # A memory of not knowing something (Delta know?)

class Gender(Enum):
    MASC = "masculine"
    FEM = "feminine"

class TokenClass(Enum):
    PERSON = "person"
