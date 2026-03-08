## todo

- apply unification in Solver:solve()

- I added `sentence` as an extra data source for `match`. This works for now, but I'm not confident it's the final solution

PAM: Willa was hungry
- match inferences voor "She picked up the Michelin guide"
    - handle pronouns like "She" and "her"
    - hoe houd ik de delen van de zin bijeen? tree structure?

PAM
- de deducties van PAM moeten een mate van onzekerheid hebben; het zijn geen zekerheden; hoe streep je hypothesen af?

## context

Work out context in inference rules:
* syntax: `name{ rule. rule. }`
* application: the rules must only be applied when context name is active

## Second order sentences

Nested sentences should not just be stored relationally, because the hierarchy matters. In relational form, the dependent form is stored as a fact, and this is wrong.

## scoped

`scoped` used to result in no new variables. This has changed. Now it does. And the tests still pass. And this has advantages, but maybe also disadvantages. Create a new predicate that explicitly exposes variables? Change the name of `scoped` to `execute`?

## multiple sentences

* the parser should always return multiple sentences, and there should be a better standard way on how to find different sentences

## inference to deduction

Everything called inference should be called deduction, to contrast it with induction.

## output

* create a separate predicate for producing output (like `output(type)`)
* or there may be different predicates `output_print()` that prints directly
* this predicate should then **wait** until the message is received by the user / client, before continuing
* this predicate can be implemented by the application in any way it sees fit

## database

- use a db like Neo4j to store second order, modal, and time-based sentences

## module

* (?) add `common_query` and `common_write` to SomeModule to reduce code duplication
* $unification of 2 variables (both should be assigned a new anonymous variable. https://www.dai.ed.ac.uk/groups/ssp/bookpages/quickprolog/node12.html)

## isolation of independent parts

optimize isolate independent parts:

* is it possible to place the independent parts directly after the head atom? faster?
* isolate the list arguments of an atom (this is not done yet)
* but: don't use isolate independent parts for predicates like "store"

## done

- remove bindings from ExecutionContext?
* $unification
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
