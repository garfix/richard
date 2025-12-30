# (
#     *DKNOW*
#     PLANNER HUM0
#     RECIPIENT HUM0
#     FACT (
#         (ACTOR HUM0 IS (*PROX* PART (*UNSPEC* CLASS (*LOCATION*))))
#         TIME (TIMK2)
#     )
# )

# DKNOW = don't know (ChatGPT)

from multiprocessing.managers import Token
from richard.processor.goal_understander.data.Fact import Fact
from richard.processor.goal_understander.data.enums import Action


class GoalStructure:
    type: Action
    planner: Token
    recipient: Token
    fact: Fact

