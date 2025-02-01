## todo

NOT_UNDERSTOOD = "Sorry, I don't understand"

^ write output

remove or()

"The answer is 10" werkt niet als de bindings uniek gemaakt worden (Solver)

* generate output
    * create unit test for sentence generator
    * the simple responder should now use a grammar
    * responder not just part of the pipeline anymore, rather part of the client
    * the sentence context is used to store buffered output
    * apply to all tests
* Read SIR thesis whole
* more SIR sentences
    * a. SET-INCLUSION ("sometimes")
    * b. SET-MEMBERSHIP (except: "the boy" without knowing what it refers to)
    * c. EQUIVALENCE no (depends on "the man" which has no reference)
    * d. OWNERSHIP
    * e. OWNERSHIP, SPECIFIC
    * f. PART-WHOLE, GENERAL
    * g. PART-WHOLE, SPECIFIC
    * h. NUMBER (done!)
    * i. LEFT-TO-RIGHT POSITION
* more SIR sentences
    * a. EXCEPTION PRINCIPLE
    * b. RESOLVING AMBIGUITIES
    * c. STREAMLINING LINKAGES
* create dialog variables for `the X`
* move the create table statements into the modules
* document
    * destructure
    * or as ;
    * grouped atoms with parens
    * replace processing exception with store output
    * generate
    * format
    * generate rules: optional atoms '?'
    * generate rules: post
    * generate rules: the order of the rules matters!
    * describe the technique of `context('question')`


## module

* (?) add `common_query` and `common_write` to SomeModule to reduce code duplication
* turn destructure2 into a more generic way of destructuring, using an array for the structure

## inferences

* create the inference structure that the second set of goals is only tried if the first fails (syntax yet unknown)

~~~
or:
    sentence_claim(Atom, "impossible") :- not(check_claim(Atom)).
    sentence_claim(Atom, "ok") :- check_claim(Atom), store(Atom).
~~~

this would be a possible implementation, but it is not clear

~~~
sentence_claim(Atom, Result) :- or(
    not(check_claim(Atom)), let(Result, "impossible"),
    store(Atom), let(Result, "ok")
).
~~~

## isolation of independent parts

optimize isolate independent parts:

* is it possible to place the independent parts directly after the head atom? faster?
* isolate the list arguments of an atom (this is not done yet)
* but: don't use isolate independent parts for predicates like "store"

## done

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
