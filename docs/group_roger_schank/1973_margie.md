# Margie (Schank, Riesbeck, Rieger, Goldman, 1973)

MARGIE parses a sentence through Riesbeck's natural language analyser. This results in a CD structure consisting of abstracted actions. It is stored in Conceptual MEMORY (Rieger). Then these structures were encoded into English sentences (Goldman, using a generator by Simmons).

MARGIE has a paraphrase and an inference mode. 

## Modules

* Conceptual analysis (Riesbeck)
* Conceptual memory and inference (Rieger)
* Conceptual generation (Goldman)

### Conceptual analysis

The parser is based on work by Winograd (SHRDLU) and Woods (LUNAR). It is an ATN (Augmented Transition Network) with semantic specialists. It produces a CD representation that contains deep semantics.

Grammar rules are implemented procedurally, not declarative. This makes the grammar hard to understand. The parser is very large (50kB) because it has rules and exceptions for every syntactic category in each of many different contexts.

Ambiguity is handled by priming: if a sentence contains the word "Racing", the preferred meaning of the word "beats" is changed to "to win" (rather than: "to hit") and this affects parsing of the next sentence.

### MEMORY

MEMORY processes the CD structure. It performs: 

* linking identifiable concepts
* establish references
* extract subpropositions
* make 5 basic inferences (normative, peripheral, causative, resolutive, predictive)
* causal chain expansion: create the inferences that lead from one fact to another. I.e. to make "Mary kissed Bill because he hit John" logical. Uses resultative and causative inferences.
* knitting: when one line of reasoning leads to the same information as another line of reasoning
* fill in concepts

It relies on 2 data types: concepts and bonds. A **bond** is a list of concepts which is stored with property BONDVALUE under a system-generated atom called SUPERATOM. A **concept** is simply a list-generated atom. Both bonds and concepts have an **occurrance set**. Each bond has a **reason set** and a **offspring set**.

## Papers

* Computer analysis of natural language in context - Riesbeck (1973)
* Inference and the computer understanding of language - Schank, Rieger (1973)
* Conceptual Memory - Rieger (1973)
* Margie memory, analysis, response generation, and inference on English - Schank, Goldman, Rieger, Riesbeck (1973)

## Books

* Conceptual information processing - Schank (1975)
