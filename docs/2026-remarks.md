## 2026-01-18

I will need to work out the thought I had yesterday, because I need it right away.

"John was lost." resolves to 

~~~js
Isolated

[
    ('resolve_name', 'John', $2)
    ('scoped', 
        [
            ('intent_understand', 
                [
                    ('lost', $2)
                ])
        ])
]

~~~

so `intent_understand`, which stores the sentence, is left with `lost($2)`, and the name of $2 ("John") is not stored in this way.

Up until now the optimized form could be used for all sentences, but this is no longer the case. It should be used only for query sentences.

I could solve this problem for the PAM system by not optimizing, but let's step back and solve it more fundamentally. Until it is solved, we will always need to choose between querying systems and story telling systems.

## 2026-01-17

I implemented unification (for example: `Atoms = lost(A)`), to make it easier to work with atom type variables.

---

It occurred to me that the SemanticComposer produces multiple versions of semantic representations, and that so far, only the last production is used by the rest of the system. However, the last production is mainly interesting for querying. It contains scoped constructs that are great for querying, but not so good for sentence analysis, such as I need for the PlanAnalyzer. Therefore it would be good to keep producing different versions of semantics, but to expose all of them for further processing.

## 2026-01-06

I'm starting the implementation of PAM with the example from chapter 14. First step: implement FIND-OUT-REQ: based on the sentence "John was lost", the system deducts that John will want to find out where he is. That is: a goal deduction rule.

## 2026-01-01

I asked Gemini for help on whom to contact for the original PAM source code. It suggested Christopher Riesbeck, one of the earliest members of the group around Shank. So I emailed him to help me find the source code. He responded by saying he didn't have any code left from that era, and that he'd also asked around. This means that I will have to re-invent the rules used to describe all domain knowledge, but at least I know that the code is not just accessible in an easy to find place. Riesbeck is also a coauthor of the book "Inside Computer Understanding: Five Programs Plus Miniatures", which contains a "micro implementation" of a.o. the PAM program. I ordered it from Amazon.

As input for PAM is complete stories, and yet they are processed one line at a time, I need the parser to be able to return multiple parse trees for a single piece of text. The parse trees it returned before are ambiguous variants. Each of these variants will now consist of multiple trees.
