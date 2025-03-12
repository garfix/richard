# Roger Schank: From CD to CBR

Systems based on theories by Roger Schank. Starting from systems working out Conceptual Dependency (CD) and ending with Case Based Reasoning (CBR) systems by Janet Kolodner.

These systems are quite modular and a specific parser may be used in several systems. I will not deal with these modules separately though, yet treat them with the system where they were first used.

## The goal of this page

Collecting all information about Schank's line of development, analysing programs, and extracting the best techniques. Extract the main line of development and collect the techniques that proved to be most useful in the end.

## Order of development

- explosion of inferences (MEMORY)
- scripts to restrict the inferences; containing roles, scenes and tracks (no way to learn similarities in scenes in different scripts), but scripts are too restrictive and don't generalize
- MOPs (Memory Organization Packets) are meant to solve this problem by reusing parts of scripts (MOPs)
- Goals and plans (to fill in the knowledge that is hard to fit in a MOP)
- TOPs: thematic structure (goals + conditions)
- CBR

## Persons

Schank starts at Yale. Wilensky starts in Yale under Schank, then sets up his own dept in Berkeley. He's not fond of MOP's developed by Schank.

Arens, Yigal                        Berkeley                PHRAN
Butler, Margaret                    Berkeley
Carbonell, Jaime                    Yale                    Politics
Cullingford, Richard                Yale                    SAM
DeJong, Gerald                      Yale                    Frump
Dyer, Michael                       Yale                    BORIS
Faletti, Joe                        Berkeley                PANDORA
Goldman, Neil                       Berkeley                MARGIE
Granacki, John                      Yale                    PHRAN
Jacobs, Paul                        Berkeley                PHRED
Kolodner, Janet
Lebowitz, Michael                   Yale, Columbia          IPP
Lehnert, Wendy                      Yale                    Qualm, Plot Units
Norvig, Peter                       Berkeley                FAUSTUS
Parker, Alice                       Yale                    PHRAN
Rieger, Charles                     Yale                    MARGIE
Riesbeck, Chris/Christopher         Yale                    MARGIE
Schank, Roger                       Yale                    __leader__
Tesler, Lawrence                    Yale                    MARGIE
Wilensky, Robert                    Yale, Berkeley          __leader__, PAM, PHRAN, Unix Consultant

## Systems

- MARGIE (1973) Schank, Goldman, Rieger, Riesbeck
- SAM (1975) Cullingford, Schank, story understanding using scripts
- PAM (1976) Wilensky, story understanding, understands the plans in a story, predicts actions based on these plans
- BELIEVER (1976) Schmidt and Sridharan - like PAM based on plans
- TaleSpin (1976) Meehan - writes stories
- FRUMP (1977) DeJong - text summarization, a bit like SAM, but skims stories using "sketchy stories"
- Qualm (1977) Lehnert, question answering for SAM and PAM
- FAUSTUS (previously: Pamela) (1983) Norvig, using frames for story understanding
- Politics (1979) Carbonell, it's about politics
- OPUS (1979) Lehnert, Burstein
- IPP (1980) Lebowitz, text skimmer - terrorism stories understander
- Plot Units (1981) Lehnert - story summary using affect
- Pandora (1982) Faletti, hierarchical planning, meta planning
- Unix Consultant (1982) - Wilensky - ask questions about UNIX
- BORIS (1982) Dyer - integration of previous structures (scripts, plans, affect); detects adages
- MOPTRANS (1984) Lytinen - translation
- KODIAK (1986) Wilensky / Berkeley - knowledge representation language
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
* TOP: thematic organization packet; defined in terms of goal situations
* TAU: thematic abstraction unit (in BORIS)

## Papers

QUALM
    The process of question-answering (PhD thesis) - Lehnert (1977)

CBR    
    Maintaining organization in a dynamic long-term memory - Kolodner (1983) 

BELIEVER    
    Recognizing plans and summarizing actions - Schmidt (1976)

Politics
    POLITICS  Automated Ideological Reasoning - Carbonel (1978)

IPP
    Memory based parsing - Lebowitz (1980?)
    Generalization and memory in an integrated understanding system (PhD thesis) - Lebowitz (1980)

Pandora
    Meta-planning: Representing and using knowledge about planning in problem solving and naturallanguage understanding - Wilensky (1981)
    PANDORA — A Program for Doing Common-sense Planning in Complex Situations - Faletti (1982)

UNIX Consultant
    Talking to UNIX in English: An Overview of a UC - Wilensky (1982)

KODIAK
     KODIAK - a knowledge representation language - Wilensky (1984)

Overview article:

Conceptual dependency and its descendants - Lytinen (1992)

## Books

Scripts Plans Goals and Understanding - Schank, Abelseon (1977)
Dynamic memory - Schank (1982)
Planning and understanding: A computational approach to human reasoning - Wilensky (1983)
Into the heart of the mind - Frank Rose,  (1984)
