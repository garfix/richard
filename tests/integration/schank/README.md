# Roger Schank: From CD to CBR

Systems based on theories by Roger Schank. Starting from systems working out Conceptual Dependency (CD) and ending with Case Based Reasoning (CBR) systems by Janet Kolodner.

## todo

- learn about CYRUS, IPP, CELIA, MOPs

## The goal of this page

Collecting all information about Schank's line of development, analysing programs, and extracting the best techniques. Extract the main line of development and collect the techniques that proved to be most useful for NLU in the end.

## Management summary

Summary of main development (with my own comments)

All systems are about making plausible inferences from the read text, in order to understand the rest of it (ie. to answer questions about it). 

* __MARGIE__ was the first system. It made a large number of undirected inferences (slow, ineffective). 
* __SAM__ used built-in __stories__, which is effective (but rigid and laborious). 
* __PAM__ deduced the __goals__ and __plans__ of agents, which is also effective. 
* __Plot units__ added __affect__ and emotion
* "Dynamic Memory" is learning new structures. 
* MOPs were invented to reuse story-parts, which makes them more flexible, simple, and reusable.
* __IPP__ is dynamic; it learns new MOPs. 
* __CYRUS__ is also dynamic. stores and retieves __events__ in Long Term Memory
* __Pandora__ creates and combines plans in order to act. "Integrated" means that all modules are active at the same time; non-sequential. 
* __BORIS__ is integrated and uses demons (hard to maintain and debug)
* __FAUSTUS__ uses frames for all inference (it's generic but less effective for scrips and plans)

## Mental phenomena

The systems in this area of research model some of the mental phenomena that humans have, in order to understand:

* Scripts: knowledge of a stereotyped event that occurs in a socially ritualized activity such as going to a restaurant and riding a subway
* Goals and Plans: states we want to achieve, and the means of getting there
* Long Term Memory (Episodic memory): a store of memories of events
* Affect / emotion

Some systems model one or more of these in a separated way, while others try to integrate multiple phenomena in a more uniform manner.

## Persons

Universities

Stanford - Stanford, California
Yale - New Haven, Connecticut
Berkeley - University of California
Georgia - Georgia Institute of Technology

Schank starts in Standford, then moves to Yale. 
Wilensky starts in Yale under Schank, then sets up his own dept in Berkeley. He's not fond of MOP's developed by Schank.

NAME                                UNIVERSITY              SYSTEM
Arens, Yigal                        Berkeley                PHRAN
Burstein, Mark                      Yale                    OPUS
Butler, Margaret                    Berkeley
Carbonell, Jaime                    Yale                    Politics
Chin, David                         Berkeley                PHRAN (Unix consultant)
Cullingford, Richard                Yale                    SAM
DeJong, Gerald                      Yale                    Frump
Dyer, Michael                       Yale                    BORIS
Faletti, Joe                        Berkeley                PANDORA
Goldman, Neil                       Stanford                MARGIE
Granacki, John                      Yale                    PHRAN
Jacobs, Paul                        Berkeley                PHRED
Kolodner, Janet                     Yale, Georgia           CYRUS
Lebowitz, Michael                   Yale, Columbia          IPP
Lehnert, Wendy                      Yale                    Qualm, OPUS, Plot Units
Lytinen                             Yale                    MOPTRANS
Meehan, James                       Yale                    Talespin
Norvig, Peter                       Berkeley                FAUSTUS
Parker, Alice                       Yale                    PHRAN
Rieger, Charles                     Stanford                MEMORY (MARGIE)
Riesbeck, Chris/Christopher         Stanford                ELI (MARGIE)
Schank, Roger                       Stanford, Yale          __leader__
Tesler, Lawrence                    Stanford                MARGIE
Wilensky, Robert                    Yale, Berkeley          __leader__, PAM, PHRAN, Unix Consultant

## Systems

Stanford
- MARGIE (1973) Schank, Goldman, Rieger, Riesbeck

Yale
  NAME (YEAR) PERSON                DATA STRUCTURE          SHORT DESCRIPTION

- SAM (1975) Cullingford            Script                  story understanding using scripts
- PAM (1976) Wilensky               Plan                    story understanding, understands the plans in a story, predicts actions based on these plans
- TaleSpin (1976) Meehan            Planning structure      writes stories
- FRUMP (1977) DeJong               Sketchy script          text summarization, a bit like SAM, but skims stories using "sketchy stories"
- Qualm (1977) Lehnert              __underlying system__   question answering frontend for SAM and PAM systems
- Politics (1979) Carbonell         Script                  about politics
- OPUS (1979) Lehnert,Burstein      Object primitive
- IPP (1980) Lebowitz               SMOP, specMOP, AUs      terrorism stories understander, learns MOPs
- Plot Units (1981) Lehnert         Plot Units              story summary using affect
- BORIS (1982) Dyer                 Affect, __many other__  integration of previous structures (scripts, plans, affect); detects adages
- CYRUS (1983) Kolodner             EMOP                    events in Long Term Memory
- CELIA
- MOPTRANS (1984) Lytinen           MOP                     multi-lingual integrated parser; translation

Berkeley
  NAME (YEAR) PERSON                DATA STRUCTURE          SHORT DESCRIPTION

- Pandora (1982) Faletti            Event,(Meta-)Goal,Plan  planning, meta planning
- Unix Consultant (1982) Wilensky   __uses Pandora__        ask questions about UNIX
- FAUSTUS (Pamela) (1983) Norvig    Frame                   integration of previous system using frames

The book "Into the heart of the mind" (Frank Rose, 1984) writes about the period in Berkeley.

Georgia
  NAME (YEAR) PERSON                DATA STRUCTURE          SHORT DESCRIPTION

- CYRUS (1983) Kolodner         EMOP

?
- BELIEVER (1976) Schmidt and Sridharan - like PAM based on plans

CBR?
Georgia
- CYRUS () Kolodner, Case Based Reasoning
- CELIA
?
- CHEF ()
- PERSUADER ()
- JUDGE ()
- MEDIATOR ()
- CABARET ()

## Representation languages

Data is stored in the system in different ways:

- Conceptual Dependency (most systems) - Schank
- KODIAK (FAUSTUS, Unix Consultant) - Wilensky

## Data structures

* Script 
* Sketchy script
* Plan
* Planning structure: delta act, package, sigma state
* Object primitive
* Goal
* Theme
* Affect
* Frame (see FAUSTUS): integration of earlier data structures like scripts, plans and goals
* Case
- Plot Unit
- Story grammar ("Once upon a time")
- Story point
* MOP: Memory Organization Packet, representation of an abstracted event
* S-MOP: Simple MOP
* spec-MOP: specialized MOP
* AUs (Action Units)
* EMOP: Episodic Memory Organization Packet
* TOP: Thematic Organization Packet; defined in terms of goal situations
* TAU: Thematic Abstraction Unit (in BORIS)

## General papers

Reading and memory organization: an introduction into MOPs - Schank (1979)
Conceptual dependency and its descendants - Lytinen (1992)

## General books

Scripts Plans Goals and Understanding - Schank, Abelson (1977)
Dynamic memory - Schank (1982)
Strategies for Natural Language Processing - Edited By Lehnert, Ringle (1982)
Planning and understanding: A computational approach to human reasoning - Wilensky (1983)
Into the heart of the mind - Frank Rose (1984)

## Papers of minor system

BELIEVER    
    Recognizing plans and summarizing actions - Schmidt, Sridharan, Goodson (1976)

FRUMP
    Prediction and Substantiation  A New Approach to Natural Language Processing (1979)

IPP
    Memory based parsing - Lebowitz (1980?)
    Generalization and memory in an integrated understanding system (PhD thesis) - Lebowitz (1980)

MOPTRANS
    The representation of knowledge in a multi-lingual, integrated parser - Lytinen (1984)

OPUS
    The role of object primitives in natural language processing - Lehnert, Burstein (1979)
    The Use of Ooject-Specl flc Knowledge in Natural Language Processing - Burstein (1979)

Pandora
    Meta-planning: Representing and using knowledge about planning in problem solving and natural language understanding - Wilensky (1981)
    PANDORA — A Program for Doing Common-sense Planning in Complex Situations - Faletti (1982)

Politics
    POLITICS  Automated Ideological Reasoning - Carbonel (1978)

QUALM
    The process of question-answering (PhD thesis) - Lehnert (1977)

Talespin
    The metanovel: writing stories by computer (PhD thesis) - Meehan (1976)

UNIX Consultant
    Talking to UNIX in English: An Overview of a UC - Wilensky, Arens, Chin (1982)
