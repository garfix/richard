## todo

- understand the story sentences, one at a time
- NB! declarative sentences -> must be stored!

Create a functional design for PAM

- the goal is to recreate the example dialogs
- to this end we recreate the program structure, algorithms and data structures
- which means we need 
    - the algorithm
    - the data stucture
    - built-in knowledge
        - if/then rules
    - the new core classes to house the algorithm

Problems

- there is not really a dialog. There's a story, questions, and asking for a summary
    - how to write the tests? how to use this structure in a conversation?
    - distinguish between statements in a story ("John robbed a liquor store") and statements to learn facts ("Sheep are mammals")
- when are the inferences made? before, during, or after excution?
    - during! we even have the inference `dialog`. we may want to add real production rules (if X then add Y and Z)
- facts are added to the dialog via declarative senstences as well
- facts should have a "likeliness" score
 
The algorithm

- is there a prediction that explains the input?
- if no: can an explanation be inferred from the input? 
- if yes: make the inference

- whenever a fact is stored (via `store`), the __production rules__ are evaluated and produce new facts
- if the fact exists already, it is not readded, and does not recheck the production rules
- production rules say: if this fact is added to the dialog, these facts should be added as well
- these rules produce themes, goals and plans
    - themes are constants (ie `hunger`)
    - if goal-condition then 
        - build a __goal episode__: (goal, goal source (theme), plan)
        - make __suggestions__ / __requests__: predictions about how the plan __gap__ will be filled: with a plan that satisfies the goal: `[((PLAN) !INPUT! SUITABLE-PLAN-RULE)]`
- each goal has a list of plans that fulfill it



## context

Work out context in inference rules:
* syntax: `name{ rule. rule. }`
* application: the rules must only be applied when context name is active

## output

* create a separate predicate for producing output (like `output(type)`)
* or there may be different predicates `output_print()` that prints directly
* this predicate should then **wait** until the message is received by the user / client, before continuing
* this predicate can be implemented by the application in any way it sees fit

## module

* (?) add `common_query` and `common_write` to SomeModule to reduce code duplication
* turn destructure2 into a more generic way of destructuring, using an array for the structure

## isolation of independent parts

optimize isolate independent parts:

* is it possible to place the independent parts directly after the head atom? faster?
* isolate the list arguments of an atom (this is not done yet)
* but: don't use isolate independent parts for predicates like "store"

## done

* replace SimpleResponder by BasicGenerator
* learn_grammar_rule
* directly execute code
* characters as tokens; exit tokenizer
* add ResultIterator
* can parsing be done faster?
* document parse tree sort heuristics
* chat-80 import csv
* optimize in-memory db
* import from csv
* can np's be implemented as atoms without find?
* optimize: reorder atoms
* inference engine
* create numbers based on a token
* create a context and pass it to each module function, in stead of the arguments which are mostly unused
* table select columns to display => intents as atoms?
* add units to scalar answers and floor floating point numbers in tables to integers
* can aggregates by simplified?
* importers based on hand-written grammar in stead of regex
* store type information with the variable in stead of an Instance?
* start using dialog variables in stead of sentence variables; it's hard to change them later
* pass variables to functions or None values?
* more access to in-between results of blocks
* added data sources for Postgres, MySQL, Sqlite3, Sparql
* simplify the responder
