## todo

* more SIR sentences?

General

* Use a real database as much as possible.
* add `common_query` and `common_write` to SomeModule to reduce code duplication
* documentation: add a section with techniques, in stead of modules

## fundamental

When concepts are added at runtime (by introducing names), isa(E1, E2) would be better than a(E2) :- b(E1), right? Find out.
The alternative can be that predicates are added at runtime: "dogs are mammals": `('mammal', E1) :- ('dog', E1).`
The alternative can also be to introduce new (lexical) grammar rules.
But what about homonimity? A concept name with multiple meanings? "bank"
Also, when introducing new concepts by name, morpheme analysis is necessary: split "oxides" into "oxide" and "s"

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
