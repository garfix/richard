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
- PAM (1976) Wilensky, story understanding, planning
- BELIEVER (1976) Schmidt and Sridharan - like PAM based on plans
- TaleSpin (1976) Meehan - writes stories
- FRUMP (1977) DeJong - text summarization, a bit like SAM, but skims stories using "sketchy stories"
- Qualm (1977) Lenhnert, question answering
- FAUSTUS / Pamela (1983) Norvig, using frames for story understanding
- Politics (1979) Carbonel
- Plot Units (1981) Lehnert - story summary
- Pandora (1982) Faletti, hierarchical planning, meta planning
- MOPTRANS (1984) Lytinen - translation
- KODIAK (1986) Wilensky
- IPP () Lebowitz, Case Based Reasoning
- CYRUS () Kolodner, Case Based Reasoning
- CHEF ()
- PERSUADER ()
- JUDGE ()
- MEDIATOR ()
- CABARET ()

## Data structures

* Script: see SAM
* Plan: see PAM
* Goal
* Theme
* Case
* MOP: representation of an abstracted event; reusable by multiple scripts. Schank's Memory Organization Packets (MOPs) are frames primarily used to represent episodic memory, that is, memories of particular events and their generalizations.
* TOP: thematic structure

## Papers

QUALM
    The process of question-answering (PhD thesis) - Lehnert (1977)

CBR    
    Maintaining organization in a dynamic long-term memory - Kolodner (1983) 

BELIEVER    
    Recognizing plans and summarizing actions - Schmidt (1976)

Overview article:

Conceptual dependency and its descendants - Lytinen (1992)

## Books

Scripts Plans Goals and Understanding - Schank, Abelseon (1977)
Dynamic memory - Schank (1982)
