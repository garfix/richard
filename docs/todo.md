## todo

* independent sub-queries (Warren)
* unit test
* better error messages
* use postgres for chat-80?
* log the time it takes to perform a block

* store type information with the variable in stead of an Instance?
* start using dialog variables in stead of sentence variables; it's hard to change them later

* improve the use of types in the modules, its sloppy
* improve grammar

* table select columns to display => intents as atoms?
* create numbers based on a token
* add units to scalar answers
* floor floating point numbers in tables to integers

* update documentation
* note that I did implement a rule ("in")

* separate folder with importers
* importers based on hand-written grammar in stead of regex
* in stead of 'vp_nosub_obj', 'vp_nosub' may be sufficient: you know that it starts with 'sub' but don't know what follows
* support for table format: select the columns, fix the None in the test; cannot use s(E1, E2) because of s(E1) -> s(E2) s(E3)
* "syn": "s(E1) -> 'what' 'percentage' 'of' np(E1) tv(E1, E2) 'each' nbar(E2) '?'",  new variables in sem are not turned into sentence variables (E3)
* create a context and pass it to each module function, in stead of the arguments which are mostly unused

## done

* can parsing be done faster?
* document parse tree sort heuristics
* chat-80 import csv
* optimize in-memory db
* import from csv
* can np's be implemented as atoms without find?
* optimize: reorder atoms
* inference engine

