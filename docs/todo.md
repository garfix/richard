* start using dialog variables in stead of sentence variables; it's hard to change them later
* support for table format: select the columns, fix the None in the test; cannot use s(E1, E2) because of s(E1) -> s(E2) s(E3)
* improve the use of types in the modules, its sloppy
* document parse tree sort heuristics
* in stead of 'vp_nosub_obj', 'vp_nosub' may be sufficient: you know that it starts with 'sub' but don't know what follows
* maybe the variable in quant is superfluous
* create numbers based on a token
* chat-80 import csv
* simplify semantics that uses EXISTS
* optimize: reorder atoms
* optimze: distinguish between all-quantors and existential quantors
* update documentation
* unit test
* better error messages
* use postgres for chat-80?
* log the time it takes to perform a block
* can parsing be done faster?
* table select columns to display => intents as atoms?
* improve grammar
* import from csv
