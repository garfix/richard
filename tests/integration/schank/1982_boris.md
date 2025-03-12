In BORIS, abstract thematic patterns, such as hypocrisy, are handled by memory structures called TAUs (Thematic Abstraction Units). These structures arise when expectation failures occur, causing episodes to be organized around errors in planning.

## Parser

"But eventually it became clear that this type of modularity had its drawbacks.
With an isolated parser, other process knowledge arising from the parsing task could
never be made available as an aid in the natural language understanding task itself.
Strict modularity was abandoned with the creation of FRUMP [DeJong, 1979b], which
relied heavily on scriptal knowledge to direct its parsing processes. Since the creation of
FRUMP, every parser at Yale has been integrated to a greater degree - each trying to
make use of task and domain specific knowledge as an aid to the parsing process."

## TAU

Taus represent planning errors

Thematic Abstraction Units share similarities with other representational systems under development at Yale, such as Schank's TOPs and Lehnert's Plot Units

Principles

* TAUs organize cross-contextual episodes which involve similar failures in planning. 
* TAUs are characterized by adages, which provide planning information
* TAUs represent one kind of story point and account for what makes some narratives memorable. 
* TAU recognition Is based on eleven planning metrics.
* Affective reactions reveal underlying goal situations at an abstract level. 
* ACEs (Affect as a Consequence of Empathy) capture the empathetic aspect of interpersonal relationships. 
* AFFECTs help signal themes Involving planning errors and expectation failures.
* Affective reactions signal situations that are important to individuals. 


In fact, TAUS appear to serve as an indexing scheme used by TOPs. So the relationship of TOPs to TAUs is analogous to that between goals and plans.

Schank has argued that episodic memory is organized, not around planning successes, but rather around their failures. Learning occurs only where failures have occurred. TAUs are more often characterized by adages which describe situations involving failures rather than successes. 

Plot Units seem to fall in between TOPs and TAUs. 

Since episodes can be indexed in terms of TAUs, and since TAUs represent planning errors, it is clear that a major aspect of TAU recognition depends on the ability to recognize planning errors when they arise. There are three situations which indicate that a planning error may have occurred: 

* goal failures
* expectation failure
* planning choices

## Processing

In BORIS, all process knowledge is implemented in the form of demons. Demons fall within the class of production systems and
are a generalization of Riesbeck's requests. Demons implement a form of delayed processing. Demons wait until their test conditions are satisfied, at which point they fire and execute their actions. Each live (active) demon is in charge of its own life cycle, deciding how long to stay alive and when to die. 

The knowledge structures they work for and the connections they form with other knowledge structures. So we have:

- GOAL/PLAN demons
- AFFECT/ACE demons
- MOP demons
- OBJECT demons
- SCRIPT/EVENT demons
- INTERPERSONAL demons
- ROLE demons
- REASONING/BELIEF demons
- THEMATIC demons
- SETTING demons

The kinds of tasks the demons must perform once their conditions have been satisfied. These include tasks such as:

- Finding references
- Binding roles
- Applying knowledge structures
- Checking presuppositions
- Instantiating episodes in memory
- Disambiguating word senses
- Noticing norm deviations
- Answering Questions


## Papers

Integration, Unification, Reconstruction, Modification: An Eternal Parsing Braid - Dyers (1981)
In-depth Understanding: A Computer Model of Integrated Processing for Narrative Comprehension - Dyer (PhD thesis, 1983)
