# PAM

From Chapter 13 in "Understanding goal-based stories"

PAM is primarily concerned concerned with using its knowledge to find explanations. An explanation consist of intentional entities. A plan explains an event, a goal explains a plan and a goal is explained by a theme, by instrumentality or by the need to subsume a recurring goal. In the course of finding these explanations, PAM may be required to spot a conflict among the characater's goals, to detect competition among the goals of different characters, or to determine that several character's goals are in concordance.

PAM’s explanation algorithm makes use of two components: A bottom—up mechanism that can make explanatory inferences from an input independent of context, and a predictive mechanism that constrains the bottom—up inference process. The predictive mechanism tries to find an intentional explanation by relating an input to the story representation. If it cannot, the bottom—up mechanism is used to suggest possible explanations for the input. The predictive mechanism then tries to find an explanation in the story representation for the inferred explanation. The cycle repeats until either a connection to the story representation is established, in which case an explanation has been found, or until no more bottom—up explanatory inferences can be drawn. In this case, the program fails to understand the input.

