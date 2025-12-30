# PAM

From Chapter 13 in "Understanding goal-based stories"

PAM is primarily concerned concerned with using its knowledge to find explanations. An explanation consist of intentional entities. A plan explains an event, a goal explains a plan and a goal is explained by a theme, by instrumentality or by the need to subsume a recurring goal. In the course of finding these explanations, PAM may be required to spot a conflict among the character's goals, to detect competition among the goals of different characters, or to determine that several character's goals are in concordance.

PAM’s explanation algorithm makes use of two components: A bottom—up mechanism that can make explanatory inferences from an input independent of context, and a predictive mechanism that constrains the bottom—up inference process. The predictive mechanism tries to find an intentional explanation by relating an input to the story representation. If it cannot, the bottom—up mechanism is used to suggest possible explanations for the input. The predictive mechanism then tries to find an explanation in the story representation for the inferred explanation. The cycle repeats until either a connection to the story representation is established, in which case an explanation has been found, or until no more bottom—up explanatory inferences can be drawn. In this case, the program fails to understand the input.

## Design

### CD

I believe the Conceptual Dependency formalism to be inessential for this problem, and more of a hindrance than a help, and I do not want to add another formalism to the one I already have, and therefore I will continue to use basic predicates.

CD makes some unneccesary assumptions that can be wrong, or are strange at best. For example: to kill someone is IS HEALTH(-10).

### Concepts

Concept|Description
-|-
event|the contents of any line in a story
plan|a way of accomplishing a goal
goal|the desired state of affairs
character|an actor with goals
story|a paragraph of text involving a purposeful interaction between characters
theme|a goal (or goal like entity) that requires no further explanation
drive|a theme like hunger, or sexual arousal
attitude|a theme like fondness towards an individual
socal role|a theme like being a garbage man
explanation|the reason why an actor of a story chose to perform a particular action
instrumentality|a goal is often instrumental to a plan for another goal
goal conflict|within a character, the fulfillment of one goal precludes the fulfillment of others (ch 6, 7)
goal competition|between two characters, whose goals interfere with one another (ch 8, 9)
goal concord|between two characters, perform actions together towards a common goal (ch 10)
goal subsumption|achieve a state that will make it easier to fulfull a recurring goal (ch 4, 5)

### Data structures

These structures are built during the processing of a text.
The structures are in a short term memory, which is not persisted to a db
But it should be possible to query this information

action

plan (planbox)
- instance of plan

goal: a single story may contain multiple goals, and these goals can interact
- status: fulfilled, abandoned, set aside
- example: John wants to have a gun

theme

goal subsumption source (p86)
- attributes:
    - recurring goal
    - source of goal
    - plan
    - precondition

**predictions**

predicted action
- a plan without an action predicts an action

predicted plan
- multiple predictions, but not yet proven
- a goal without a plan predicts a plan

predicted goal
- a theme without a goal predicts a goal

predicted theme

**objects**

object knowledge
- the use of a bicycle is to be ridden
- the function of an object is a description of the plans for which that object was designed
- consumable?

### Knowledge structures

Stored knowledge about plans and goals

goals
- preserving his right to drive
- the cop not to give him a summons
- a goal may be recurring (pay the rent)

plans
- asking, bargaining
- OVERPOWER (goal = to get something from someone)
- planning for frequently reoccurring goals (ch 4 & 5)
- planning with conflicting goals (ch 6 & 7)
- what plans can characters with concordant goals use to aid each other? (ch 10)

goal relationships (p19)
- relations between goals

resources (p116)
- time
- consumable functional objects
- non-consumable functional objects
- abilities

**recognition rules / requests**

plan-recognition rules
- general: if event A causes event B, then a way to prevent B is to prevent A
- a person may want to harm someone he greatly dislikes
- if a person loves someone, then he will want to help that person if that person is endangered
- knowing the location is instrumental to going there
- attached to "gun": predict the THREATEN or OVERPOWER plans

goal-recognition rules
- if A "wants B's C" then taking control of B' C is a goal of A

theme-recognition rules (from goal to theme)
- if a person wants to possess an object, then he may have the attitude of liking the object
- if a person wants to possess an object that has a function, then he may want to use that object to perform its function

goal-subsumption state recognition (4.3)
- types
    - establishment
    - replacement
    - termination
- if a character has a negative attitude toward an action that may be dominated by a recurring goal, then that character may want to subsume the recurring goal using a plan that does not involve the distasteful acion (p94)
- more rules: p105

goal conflict detection rules (p118)

goal abandonment recognition rules (p136)

**other**

goal-interaction rules
- idem: declarative or procedural

subsumption state
- ownership of a functional object
- tapping a stream
- being in a social relationship
- knowing something

### Reading algorithm

the story reader's main job is to understand the goals of each character in the story
inferring the plans each character is using to achieve the goals
noticing how characters' goals relate to one another: recognize that goals are in concord, conflict, etc

two aspects
- bottom-up
- predictive

my comments on bottom-up
- why did character A do that? what goal is involved?
- find out character's goals and plans
- reason about motives
- find explanation for event
- determine if a goal is fulfilled, abandoned, set aside
- how to determine which plan is used?

my comments on predictive 
- see if the next input is a response to a question
- predictions should be specific, don't just make all possible predictions
- predictions can be made about the goals or plans that will be inferred later on in the story
- check if a prediction is confirmed
- predictions can be used to constrain the bottom-up inference process without eliminating it entirely

Wilensky:
- read line of text
- turn text into semantic representation
- find an explanation for an event
    - step 1: is the event part of a known plan? yes => the plan is the explanation
    - step 2: no => can a plan (or plans) be inferred from the event? no => fail
    - step 3: can one of these plans be a plan for a known goal? yes => the plan is the explanation
    - step 4: can a goal (or goals) be inferred from one of the plans? no => fail
    - step 5: can one of these goals be instrumental to a known plan?  yes => the plan-goal sequence is the explanation
    - step 6: can one of these goals have arisen because of a known theme? yes => plan-goal-theme is the explanation
    - step 7: can a plan be inferred to which one of these goals is instrumental? no => fail
    - goto step 3
- subsumption state recognition algorithm (p89)
    - step 1: does the state at which the goal is aimed normally subsume any goals? no => the expection has not been met
    - step 2: are any of these goals the same as the goal the planner is trying to subsume? yes => the expection has been confirmed
    - step 3: could one of these goals be instrumental to the goal the planner is trying to subsume? yes => the expection has been confirmed
    - the expectation has not been met
- goal conflict recognition algorithm (p114)
    - does the new goal require a resource also required by another goal and of which there is an insufficient quantity? yes => the new goal conflicts with an old goal
    - does the fulfullment of the new goal entail the creation of a state that is mutually exclusive with a state needed for another goal? yes => the new goal conflicts with an old goal
    - does the fulfillment of the new goal entail the generation of a preservation goal? yes => the new goal conflicts with the preservation goal
    - the new goal does not cause a goal conflict
- detecting a conflict caused by a limited resource (p117)
    - does the story suggest a scarce resource? no => no conflict
    - infer the plan usually used for each goal
    - is the resource common to each plan? no => no conflict
    - is the amount available less than the amount needed? no => no conflict
    - there exists a conflcit due to resource limitations

- top down
    - try to match a prediction
- bottom-up
    - try to match one of the event-goal rules to find a goal
        - goal found? 
            - find an explanation for the goal, and a theme for the goal
            - add a predicted plan for the goal to memory
            - add a predicted theme for the goal to memory


my findings
- read a line of text
- pronoun resolution ("he")
- bottom-up
    - make some standard inferences ("John" is a man)
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
- a confirmation of a prediction causes another prediction to be set up looking for yet another plan

TODO: add explanatory diagrams for each of the actions in the algorithm
