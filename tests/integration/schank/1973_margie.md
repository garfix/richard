# Margie (Schank, Riesbeck, Rieger, Goldman, 1973)

MARGIE parses a sentence through Riesbeck's natural language analyser. This results in a CD structure consisting of abstracted actions. It is stored in Conceptual MEMORY (Rieger). Then these structures were encoded into English sentences (Goldman, using a generator by Simmons).

## Modules

* Conceptual analysis (Riesbeck)
* Conceptual memory and inference (Rieger)
* Conceptual generation (Goldman)

### MEMORY

MEMORY is part of MARGIE. Processes the incoming parsed CD structure. It performs: linking identifiable concepts, establish references, extract subpropositions, make 5 basic inferences (normative, peripheral, causative, resolutive, predictive), causal chain expansion, knitting, fill in concepts. It relies on 2 data types: concepts and bonds. A bond is a list of concepts which is stored with property BONDVALUE under a system-generated atom called SUPERATOM. A concept is simply a List-generated atom. Both bonds and concepts have an **occurrance set**. Each bond has a **reason set** and a **offspring set**.

## Papers

* Computer analysis of natural language in context - Riesbeck (1973)
* Inference and the computer understanding of language - Schank, Rieger (1973)
* Conceptual Memory - Rieger (1973)
* Margie memory, analysis, response generation, and inference on English - Schank, Goldman, Rieger, Riesbeck (1973)

## Books

* Conceptual information processing - Schank (1975)
