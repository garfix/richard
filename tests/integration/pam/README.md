# PAM

From Chapter 13 in "Understanding goal-based stories"

PAM is primarily concerned concerned with using its knowledge to find explanations. An explanation consist of intentional entities. A plan explains an event, a goal explains a plan and a goal is explained by a theme, by instrumentality or by the need to subsume a recurring goal. In the course of finding these explanations, PAM may be required to spot a conflict among the character's goals, to detect competition among the goals of different characters, or to determine that several character's goals are in concordance.

PAM’s explanation algorithm makes use of two components: A bottom—up mechanism that can make explanatory inferences from an input independent of context, and a predictive mechanism that constrains the bottom—up inference process. The predictive mechanism tries to find an intentional explanation by relating an input to the story representation. If it cannot, the bottom—up mechanism is used to suggest possible explanations for the input. The predictive mechanism then tries to find an explanation in the story representation for the inferred explanation. The cycle repeats until either a connection to the story representation is established, in which case an explanation has been found, or until no more bottom—up explanatory inferences can be drawn. In this case, the program fails to understand the input.

## Design

### Concepts

Concept|Description
-|-
character|an actor with goals
story|a paragraph of text involving a purposeful interaction between characters
event|
plan|a way of accomplishing a goal
goal|the desired state of affairs
theme|

reccurring goals (ch 4, 5)
goal conflict (ch 6, 7)
goal competition (ch 8, 9)
goal concordance (ch 10)

### Data structures

These structures are built during the processing of a text.
The structures are in a short term memory, which is not persisted to a db

events (based on existing tech)

character goal: a single story may contain multiple goals, and these goals can interact
- status: fulfilled, abandoned, set aside
- example: John wants to have a gun

character plan (planbox)
- instance of plan

predicted character plans
- multiple predictions, but not yet proven

predicted character goals


### Knowledge structures

Stored knowledge about plans and goals

goals
- preserving his right to drive
- the cop not to give him a summons

plans
- asking, bargaining
- OVERPOWER (goal = to get something from someone)
- planning for frequently reoccurring goals (ch 4 & 5)
- planning with conflicting goals (ch 6 & 7)
- what plans can characters with concordant goals use to aid each other? (ch 10)

goal relationships (p19)
- relations between goals

some sort of deduction
- general: if event A causes event B, then a way to prevent B is to prevent A
- a person may want to harm someone he greatly dislikes
- if a person loves someone, then he will want to help that person if that person is endangered
- knowing the location is instrumental to going there

plan-recognition rules
- attached to "gun": predict the THREATEN or OVERPOWER plans
- is this knowledge declarative or procedural (i.e. part of the reading algorithm?)
- how to recognize a plan

goal-interaction rules
- idem: declarative or procedural

### Reading algorithm

the story reader's main job is to understand the goals of each character in the story
inferring the plans each character is using to achieve the goals
noticing how characters' goals relate to one another: recognize that goals are in concord, conflict, etc

two aspects
- bottom-up
- predictive

bottom-up comments
- why did character A do that? what goal is involved?
- find out character's goals and plans
- reason about motives
- find explanation for event
- determine if a goal is fulfilled, abandoned, set aside
- how to determine which plan is used?

predictive comments
- see if the next input is a response to a question
- predictions should be specific, don't just make all possible predictions
- predictions can be made about the goals or plans that will be inferred later on in the story
- check if a prediction is confirmed
- predictions can be used to constrain the bottom-up inference process without eliminating it entirely

algorithm
- read a line of text
- pronoun resolution ("he")
- bottom-up
    - recognize a goal ("John wanted some money")
        - infer higher-up other possible goals from this goal (goal subsumption)
    - recognize an event ("he got a gun")
        - infer an anonymous plan (how he got the gun)
        - infer a goal from an event ("to have a gun")
            - infer possible plans for the goal ("gun": THREATEN, OVERPOWER)
                - infer possible goals for the plan (to get something (some money) from someone)
    - recognize an event ("and walked into a liquor store")
        - infer based on prediction (*somehow infer that John want to rob the liquor store)
- predictive
    - after inferring the goal (to get something (some money) from someone)
        - predict the execution of the plan (to threaten or overpower someone to get the money)
