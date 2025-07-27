# (
#     *GOAL-EPISODE*
#     GOALFORM (
#         GOAL (
#             *DKNOW*
#             PLANNER (NIL)
#             RECIPIENT (NIL)
#             FACT (NIL))
#         SOURCE (NIL)
#         RELATIONS (*LIST*)
#         OUTCOME (NIL))
#     ATTEMPTS (*LIST*)
# )


from richard.processor.goal_understander.data.Attempt import Attempt
from richard.processor.goal_understander.data.GoalForm import GoalForm


class GoalEpisode:
    type: str
    goal_form: GoalForm
    attempts: list[Attempt]
