# Roger Schank: From CD to CBR

Systems based on theories by Roger Schank. Starting from systems working out Conceptual Dependency (CD) and ending with Case Based Reasoning (CBR) systems by Janet Kolodner.

These systems are quite modular and a specific parser may be used in several systems. I will not deal with these modules separately though, yet treat them with the system where they were first used.

## The goal of this page

Collecting all information about Schank's line of development, analysing programs, and extracting the best techniques. Extract the main line of development and collect the techniques that proved to be most useful in the end.

## Order of development

- explosion of inferences (MEMORY)
- scripts to restrict the inferences; containing roles, scenes and tracks (no way to learn similarities in scenes in different scripts)
- MOPs (Memory Organization Packets)
- Goals and plans (to fill in the knowledge that is hard to fit in a MOP)
- TOPs: thematic structure (goals + conditions)
- CBR

## Systems

- MARGIE (1973) Schank, Goldman, Rieger, Riesbeck
- SAM (1975) Cullingford, Schank, story understanding
- PAM (1976) Wilensky, story understanding
- BELIEVER () Schmidt and Sridharan
- FRUMP () DeJong
- TaleSpin (1976) Meehan
- Qualm (1977) Lenhnert, question answering
- Pamela (1978) Norvig, story understanding
- Politics (1979) Carbonel
- Plot Units (1981) Lehnert
- Pandora (1982) Faletti, story understanding
- IPP () Lebowitz, Case Based Reasoning
- CYRUS () Kolodner, Case Based Reasoning
- CHEF ()
- PERSUADER ()
- JUDGE ()
- MEDIATOR ()
- CABARET ()

## Abbrebiations

CP = Conscious Processor (the mind of some person)
PP = Picture Producer: people and things that fill a slot in a script. May be a single entity or a group.

## Concepts

**Causal chain expansion** create the inferences that lead from one fact to another. I.e. to make "Mary kissed Bill because he hit John" logical. Uses resultative and causative inferences.

**Knitting** when one line of reasoning leads to the same information as another line of reasoning

Goal, Plan, Theme, Case

## Papers


1977b: The process of question-answering (PhD thesis) - Lehnert (1977)

1983a: Maintaining organization in a dynamic long-term memory - Kolodner (1983) 

Overview article:

Conceptual dependency and its descendants - Lytinen (1992)

## Critiques on the original work

- The basic actions are ad-hoc and lack some of the detail of the original verbs
- the parser creates a semantic representation that assumes a conceptual framework
- Scripts can be inflexible. To deal with inflexibility, smaller modules called memory organization packets (MOP) can be combined in a way that is appropriate for the situation. [https://en.wikipedia.org/wiki/Script_theory]
