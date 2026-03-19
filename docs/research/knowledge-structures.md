What kind of knowledge structures allow for second order sentences

* John wants [that Jane does her homework]
* Pick up at least three boxes if there's a green block behind a red pyramid

Results from Claude

## Relational

    name($1, "John")
    name($2, "Jane")
    want($e1, $1, $e2)
    do_homework($e2, $2)

## DRT

Inner DRSs are boxed sub-structures, allowing quantification and anaphora resolution across scope boundaries. Very influential in NLP.

John wants [that Jane does her homework]:

    [x: John | WANT(x, [y: Jane | DO-HOMEWORK(y)])]

Pick up at least three boxes if there's a green block behind a red pyramid    

    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │  ╔══════════════════════════╗                       │
    │  ║ CONDITION BOX            ║                       │
    │  ╠══════════════════════════╣                       │
    │  ║  y, z                    ║                       │
    │  ╠══════════════════════════╣                       │
    │  ║  block(y)                ║                       │
    │  ║  green(y)                ║                       │
    │  ║  pyramid(z)              ║                       │
    │  ║  red(z)                  ║                       │
    │  ║  behind(y, z)            ║                       │
    │  ╚══════════════════════════╝                       │
    │            ⇒                                        │
    │  ╔══════════════════════════╗                       │
    │  ║ CONSEQUENCE BOX          ║                       │
    │  ╠══════════════════════════╣                       │
    │  ║  X                       ║  ← X is a set         │
    │  ╠══════════════════════════╣                       │
    │  ║  box(X)                  ║                       │
    │  ║  |X| ≥ 3                 ║                       │
    │  ║                          ║                       │
    │  ║  ┌──────────────────┐    ║                       │
    │  ║  │ x                │    ║                       │
    │  ║  │──────────────────│    ║                       │
    │  ║  │ x ∈ X            │    ║                       │
    │  ║  │ pick_up(sys, x)  │    ║                       │
    │  ║  └──────────────────┘    ║                       │
    │  ╚══════════════════════════╝                       │
    │                                                     │
    └─────────────────────────────────────────────────────┘    

## AMR

AMR uses role-value graphs with special :ARG relations:

John wants [that Jane does her homework]:

    (w / want-01
    :ARG0 (j / person :name "John")
    :ARG1 (d / do-02
                :ARG0 (n / person :name "Jane")
                :ARG1 (h / homework)))

Pick up at least three boxes if there's a green block behind a red pyramid                

    (c / conditional
    :condition (e / exist-01
                    :ARG1 (b / block
                                :mod (g / green)
                                :location (b2 / behind
                                            :op1 b
                                            :op2 (p / pyramid
                                                    :mod (r / red)))))
    :consequence (p2 / pick-up-01
                        :ARG0 (s / system)
                        :ARG1 (b3 / box
                                :quant (a / at-least
                                            :op1 3))))                

## DRT meets AMR

Suggestion from Claude, emphasizing storage in a relational db.

"Every knight who served John wants Jane to do her homework"

    prop_1: { predicate: SERVE, agent: ?x,  object: John }
    prop_2: { predicate: WANT,  agent: ?x,  modality: DESIRE,
            content: prop_3 }
    prop_3: { predicate: DO,    agent: Jane, object: homework }

    quant_1: { var: ?x, restrictor: prop_1, scope: prop_2,
            type: UNIVERSAL }

## Conceptual dependency

    [
        predicate: want,
        subject: [
            name: "John"
        ]
        object: [
            predicate: "do_homework"
            subject: [
                name: "Jane"
            ]
        ]
    ]

## Frame / struct

    {
    "mood": "CONDITIONAL",
    "modality": "INDICATIVE",
    "condition": {
        "mood": "DECLARATIVE",
        "predicate": "EXIST",
        "quantifiers": [
        {
            "var": "?y",
            "type": "EXISTENTIAL",
            "restrictor": {
            "predicate": "IS",
            "agent": "?y",
            "properties": ["GREEN", "BLOCK"]
            }
        },
        {
            "var": "?z",
            "type": "EXISTENTIAL",
            "restrictor": {
            "predicate": "IS",
            "agent": "?z",
            "properties": ["RED", "PYRAMID"]
            }
        }
        ],
        "scope": {
        "predicate": "BEHIND",
        "agent": "?y",
        "theme": "?z"
        }
    },
    "consequence": {
        "mood": "IMPERATIVE",
        "predicate": "PICK_UP",
        "agent": "SYSTEM",
        "quantifiers": [
        {
            "var": "?x",
            "type": "COUNT",
            "count": 3,
            "count_mod": "AT_LEAST",
            "restrictor": {
            "predicate": "IS",
            "agent": "?x",
            "properties": ["BOX"]
            }
        }
        ],
        "arguments": [
        { "role": "PATIENT", "value_type": "VARIABLE", "variable": "?x" }
        ]
    }
    }

## Possible Worlds Semantics

Originating with Kripke and Montague, propositional attitudes are modeled as relations to sets of possible worlds:

    wants(John, W)

where W = {worlds in which Jane does her homework} Used in DRT, HPSG, and LFG formalisms at the semantic interface
