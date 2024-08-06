## todo

* optimize: reorder atoms
* optimze: distinguish between all-quantors and existential quantors
* create numbers based on a token
* simplify semantics that uses EXISTS
* update documentation
* unit test
* better error messages
* use postgres for chat-80?
* log the time it takes to perform a block
* table select columns to display => intents as atoms?
* improve grammar
* floor floating point numbers in tables to integers
* note that I did implement a rule ("in")
* separate folder with importers
* in stead of 'vp_nosub_obj', 'vp_nosub' may be sufficient: you know that it starts with 'sub' but don't know what follows
* improve the use of types in the modules, its sloppy
* support for table format: select the columns, fix the None in the test; cannot use s(E1, E2) because of s(E1) -> s(E2) s(E3)
* start using dialog variables in stead of sentence variables; it's hard to change them later
* maybe the variable in quant is superfluous (yes, may be left out)
* "syn": "s(E1) -> 'what' 'percentage' 'of' np(E1) tv(E1, E2) 'each' nbar(E2) '?'",  new variables in sem are not turned into sentence variables (E3)
* create a context and pass it to each module function, in stead of the arguments which are mostly unused
* can np's be implemented as atoms without find?

## done

* can parsing be done faster?
* document parse tree sort heuristics
* chat-80 import csv
* optimize in-memory db
* import from csv
