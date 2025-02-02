## todo

NOT_UNDERSTOOD = "Sorry, I don't understand"
^ write output

error message parsing sentence: could not understand: i

* more SIR sentences
    * b. RESOLVING AMBIGUITIES
* move the create table statements into the modules
* document
    * replace processing exception with store output
    * generate
    * format
    * generate rules: optional atoms '?'
    * generate rules: post
    * generate rules: the order of the rules matters!
    * describe the technique of `context('question')`
    * learning general rules


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
