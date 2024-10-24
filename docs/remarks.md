## 2024-10-24

salt is an element

This is derived from

* salt is a compound
* elements are not compounds

The last rule is ambiguous; it could mean:

* something is not a compound if it is an element
* something is not an element if it is a compound

and probably both are true, because this is a statement of mutual exclusion. It is the last one that is needed here.

## 2024-10-23

anything that is not a compound is not ferrous sulfide

Another "every" sentence, so its reverse should be false

nothing that is not a compound is ferrous sulfide

## 2024-10-21

oxides are not white

This means: "all oxides are not white", or "no oxide is white", or "E is an oxide and E is white: is false".

The statement is categoric (holds for all entities), but in order to test it, we need to single out a single entity, or we may end up with some entities that apply and others that don't. So if we say "E is an oxide and E is white", that should not occur, so we state that this is false. If it doesn't occur the response would be "unknown", but if it does occur, the statement is false.

===

magnesium oxide is an oxide

simple

===

every oxide is an oxide

With "every" statements, when we test we might find that some oxides are oxides and others aren't; and what to respond then? So we try to find the exception and from failing to find it we conclude that the statement is true. I have to add that this is not really a deduction one can make in an open world hypothesis.

However this is not a usual "every" statement. This one's a priori true. It's a tautology. But to treat it as a tautology we should recognize it as such.

However, howver, this is not what Cooper does. He deduces the fact that every oxide is an oxide from the fact that magnesium oxide is an oxide (11). This deduction can only be made in closed world.

When you read his comments, what he really does is make the tautology, but he says that one can only say something about oxides it there are such things as oxides. And he uses the statement "magnesium oxide is a white metallic oxide" to prove that there are oxides.

Cooper notes: "in Lukasiewicz's formulation, sentences of the form Axx and Ixx are taken to be tautologously true"

Our library can't express the tautology of the sentence, but is nevertheless able to pass the sentence.

===

some sulfides are brittle

Cooper's system deduces from the name "ferrous sulfide" that this is a sulfide.

Can be solved like this:

    { "syn": "noun(E1, T1) -> proper_noun(E1) proper_noun(E1)", "sem": lambda proper_noun1, proper_noun2: [('resolve_name', proper_noun1 + " " + proper_noun2, E1)] },
    { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    { "syn": "proper_noun(E1) -> 'sulfide'", "sem": lambda: 'sulfide', "inf": [("sulfide", e1, 'true')],},

That is: "ferrous sulfide" consists of two proper nouns. The first is free-form. The second is from a fixed group, and implies a certain type. That the second name is "sulfide" implies ("inf") that this entity is a sulfide.


## 2024-10-20

I finally got on track to the right algorithm for David Warren's isolate independent parts. I reread his article of the 20th time and then my eye fell on this little sentence:

"Once the first goal has been solved, the rest of the body breaks down in ... independent parts, neither of which share uninstantiated variables with each other or with the head of the clause"

The algorithm is now simpler, faster, and easier to understand. It is also more in line with the sort by cost algorithm. First find the first atom, then do the rest. It also makes the Chat-80 replication a bit faster even (0.246 > 0.23 s)

## 2024-10-05

no metal is a nonmetal
    ('isa', $E1, 'nonmetal, "false") :- ('isa', E1, 'metal', "true").


magnesium is a nonmetal
    Q: ('isa', $M, 'nonmetal, $R)

    A: ('isa', $E1, 'nonmetal, "false") :- ('isa', E1, 'metal', "true").
       ('isa', $M, 'metal', "true")

===

magnesium is not a nonmetal
    Q: ('isa', $M, 'nonmetal, $R) ('not_3v', $R, $S)


## 2024-10-02

There is another form possible, where each predicate directly includes its three-valued truth value:

    isa(E1, E2, Tv)

To negate it, the this predicate can be used

    not_3v(In, Out)

## 2024-10-01

"magnesium is not a nonmetal". Semantics: `knows(negate(isa($M, $NM), "true"), "true")` where `$M` is the id for magnesium and `$NM` for nonmetal.

    knows(isa($M, $NM), Tv1) negate(Tv1, Tv2)

## 2024-09-28

"magnesium is a metal" is simple in both closed world and open world.

"magnesium is not a metal" is simple in closed world. In open world you need to prove `negate(metal($M))`.

I'm adding a predicate `negate` that acts like `not` but operates on a single atom in stead of a list. If `metal($M)` has results then `negate` returns no results. No results here means: false. But if `metal($M)` has no results, this means "I don't know" and `negate` would also need to return "I don't know".

Based on a suggestion of ChatGPT I'm adding a predicate `knows(atoms, E1)` that returns one of 3 values in `E1`: False, True, or "UNKNOWN".

## 2024-09-26

magnesium is not a metal
~metal(magnesium)

Ways to write "not"

~~~python
    ("!white", E1)
    ("-white", E1)
    ("~white", E1)
    ("not white", E1)
    ("not", ("white", E1))
    negate(("white", E1))
    ("not_white", E1)
~~~

negate(("white", E1))
=>
("not_white", E1)


negate(("not_white", E1))
=>
("white", E1)

This is about storing negative information. Needs to be stored in a table, with a name. Might as well call it `not_X`.


## 2024-09-21

So Cooper's system presumes open world, but our system is closed world. What to do?

1. Allow our system to be open world as well
2. See if we happen to be able solve Cooper's dialog in our closed world system

1 seems really hard. Let's start with 2, with a tricky sentence

    anything that is not a compound is not ferrous sulfide

It's a tricky sentence, but in the current system it should be implemented as

    all(E1,
        [ thing(E1) not([compound(E1)]) ],
        [ resolve_name('ferrous sulfide', E2) not(['==', E1, E2]) ]
    )

Notice first that `thing(E1)` matches every entity in the database(!), but that it must be placed before `not([compound(E1)])` or no entities will be found at all.

The range part of all will basically result in all elements (non-compounds) in this database. As ferrous sulfide is a compound it will pass the body and the query will succeed.

As the dialog doesn't really contain that many different examples, being able to handle this sentence means that the system as is can handle Cooper's dialog in a closed world assumption.

Sentences like "dark-gray things are not white" and "no metal is a nonmetal" are silly in a closed world assumption. They may be left out, or given null-semantics.

Should we than care that it actually has an open world assumption? That's my question now. Maybe we should.

When I ask ChatGPT about open world systems it mentions all kinds of systems as open world, including Prolog. What it says is: if Prolog returns no results this _means_ that it doesn't know. Even if it _says_ `false` it means it doesn't know. And that's an interesting point because we could say that the system just returns what it knows. How this is presented is up to the response module of the system.

A yes/no question could become a "yes/i don't know" question. An answer about the number of children could be "I know of 1 child, but there could be more. Or less, if my knowledge is inaccurate." An answer about an aggregate could be: "The average is 35.1 based on the knowledge I have, but I could be missing something"

This sounds like I'm joking, but in some systems this kind of honesty may actually be appreciated.

===

Even though the sentences in this dialog may be answers using a closed world assumption, I will in fact try to solve them using an open world assumption, just like Cooper intended. It's theoretically interesting, and if there are real world use cases for it, it's good to be prepared.

This means for an answer to be "no" there must be a result that is negative, rather than no results.

===

"ferrous sulfide" is an __open compound noun__, and the system expects us to interpret the last word as a separate predicate:

    sulfide(X)

If something is called a sulfide then it is a sulfide.

===

I will be using two grammars in stead of one with conditions per rule, because the use case is not strong enough to introduce such a big new addition. Also, it makes the grammar depend on the dialog context, and before I do that I want a better used case.

## 2024-09-20

Ways to write "not"

~~~python
    ("!white", E1)
    ("-white", E1)
    ("~white", E1)
    ("not white", E1)
~~~

===

I am copying some information from an NLI-GO markdown about Strong negation:

Strong Negation

Atoms can also take a negative form

    `-predH(A, B)` :- predI(A, C) -predJ(C, B);

The interpretation of this rule is:

1) I believe `predH(A, B)` to be false if I believe `predI(A, C)` to be true and `predJ(C, B)` not to be true

Example interpretations of `-predH` are "it does not rain", "is not red", "is not on". This kind of negation is different from `not` above. Whereas `not` inverts `known`/`unknown`, `-` inverts the meaning of the predicate itself. `-raining()` means "dry or foggy or whatever, but not raining". It means "everything else". `-red` means "blue, yellow, green, purple, etc, etc" It is an affirmation of the positive belief to the complement of the original predicate: "I believe `-predH()` to be true".

In a Closed World `-` and `not` come down to the same thing, since it assumes that what is unknown is also untrue. NLI-GO takes a broader view in order to deal with the full power of natural language. It takes the Open World view.

However, when Open World proves to be too unrestrictive for a use case, you can make exceptions, and say: "for this type of predicates I need to closed world". Here's an example:

    `-predH(A, B)` :- not(predH(A, B));

This means simply: I believe `predH(A, B)` to be false if I have no knowledge about `predH(A, B)`. Examples are abound: if I can't find a reservation for customer C, I believe he has not made a reservation. (Full open world would have leave you in doubt as to wether the reservation had been made.)

More about this form of negation, called "strong negation" can be read [on Wikipedia](https://en.wikipedia.org/wiki/Stable_model_semantics#Strong_negation)

So when do you use `not` and when `-`?

* Use `not` when you mean "failed" (if it's a goal) or "not found"/"not proven" (if it's a statement)
* Use `-` when you mean "know not to be the case"; this operator is not applied to goals

==========================================

I have a big problem with "sodium chloride is an element".

It is proven by the fact that is it a compound, and therefore not an element. But it can be more easily proven through a missing `element()` fact.

Cooper's system is using an open world assumption where something needs to be explicitly disproven. Not true is different from not known.

The closed world assumption is so implicit in Prolog-like systems that can even forget to mention it.

The only use for strong negation is in being able to create exceptions to rules.

## 2024-09-19

How to implement "sodium chloride is salt"? I think the only way to make this useful for queries is to use the same dialog ID for both names.

Let's first introduce "salt"

"salt is a compound"

    resolve_name("salt", E1) store(('compound', e1))

`e1` is the variable `$7` for example; as a value it is '$7'. `resolve_name` tries to find a tuple `name(X, 'salt')`. When found, it returns the value of `X`. If not found, it creates and stores the tuple `name('$7', 'salt')` and returns '$7'.

Next introduce "natrium chloride" as a synonym for "salt".

"sodium chloride is salt"

    resolve_name("salt", E1) store(('name', "sodium chloride", e1))

`resolve_name` now returns `$7` (found in the database tuple `name('$7', 'salt')`), and stores a new name that links to the same dialog entity `('name', '$7', 'sodium chloride')`

Note that the first name, "sodium chloride" is interpreted as just a `token`, while the second name, "salt", is interpreted as a `resolve_name` atom.

## 2024-09-18

The name "magnesium" is to be implemented as an entity, with an id (let's say "magnesium"). It's not a predicate (`magnesium(E)`).

The id is found by performing `resolve_name`, where the id can simply equal the name. No need to make it more complicated.

About "burns rapidly". Here "rapidly" is an adverb to "burns". "burns" doesn't mean it's burning, but that it "can burn". So that's a capacity. "Rapidly" would be an adverb to that capacity. Cooper himself did not go into this complexity himself, and turned "burn rapidly" into a verb:

    (4) V = {#BURNS, #BURNS#RAPIDLY, #BURN, #BURN#RAPIDLY}

It's hard to do full justice to this adverb here. Also, the Cooper system is not really about this kind of thing, so making this complicated here will distract a bit on the essence of the system. We'll just introduce the predicate `burns_rapidly`.

Types of sentences to be solved, together with possible productions

- ferrous sulfide is a dark-gray compound that is brittle
    - `dark_gray('ferrous sulfide') compound('ferrous sulfide') brittle('ferrous sulfide')`
- magnesium burns rapidly
    - `burn_rapidly('magnesium')`
- gasoline is combustable
    - `combustable('gasoline')`
- combustable things burn
    - `burns(E1) :- combustable(E1) thing(E1)`
- elements are not compounds
    - `!compound(E1) :- element(E1). !element(E1) :- compound(E1).`
- no metal is a nonmetal
    - `!nonmetal(E1) :- metal(E1)`
- dark-gray things are not white
    - `!white(E1) :- dark_gray(E1)`
- any thing that burns rapidly burns
    - `burn(E1) :- burn_rapidly(E1)`

The others are variants on these.

To decide how to implement the negative rules, we'll check how they're used.

- magnesium is not a metal
    - `not(metal('magnesium'))`

- sodium chloride is an element
    - sem: `resolve_name('sodium chloride', E1) element(E1)`
    - solving:
        - `not element($7) :- compound($7)`
        - `compound($7)`


## 2024-09-17

Releases version 0.3. Started replication of Cooper's system. It has sentences that can either be statements of yes/no questions ("magnesium is a metal"). One interpretation is used by the administrator. The other by the end-user. I can do two things:

- create a separate grammar for each role
- create a context for the grammar rules. perhaps in the form of if-clauses that are part of the rule

I kind of like the last idea.

## 2024-08-28

I built a caching mechanism in `isolated`. That mainly helps for the borders-borders-borders queries where the same country reoccurs in multiple relations. Many tweaks can be made in the code things faster, but for now the performance will do. All Chat-80 queries together run in 0.23 seconds, which is much slower than in the SWI Prolog implementation, but it is much faster than what I started with (40 sec).

## 2024-08-23

I needed a way to explicitly express the result variables of a sentence and I did this by allowing `s(E1, E2, E3)`, i.e. `s` can now have multiple variables. These variables serve as the result variables needed for the isolated parts algorithm. I did this by adding an extra layer of basic rewrites:

    # gamma(G) -> delta(D)

    # delta(D) -> s(P1)
    # delta(D) -> s(P1, P2)
    # delta(D) -> s(P1, P2, P3)
    # delta(D) -> s(P1, P2, P3, P4)
    # delta(D) -> s(P1, P2, P3, P4, P5)

Quite happy with this solution.

## 2024-08-19

Start with Warren's isolating independent parts. Warren describes how to separate the independent parts, but doesn't describe how to process these parts.

I'm using these slow queries as examples:

[A] ["What is the ocean that borders African countries and that borders Asian countries?", "indian_ocean"],

    [
        ('ocean', $1)
        ('borders', $1, $2)
        ('african', $2)
        ('country', $2)
        ('borders', $1, $3)
        ('asian', $3)
        ('country', $3)
    ]

54 msecs

[B] ["What are the countries from which a river flows into the Black_Sea?", "romania, soviet_union"],

    [
        ('resolve_name', 'Black_Sea', $6)
        ('river', $5)
        ('country', $4)
        ('flows_from_to', $5, $4, $6)
    ]

80 msecs


[C] ["What are the continents no country in which contains more than two cities whose population exceeds 1 million?", "africa, antarctica, australasia"],

    [
        ('continent', $7)
        ('none',
            [
                ('country', $8)
                ('in', $8, $7)
                ('det_greater_than',
                    [
                        ('city', $9)
                        ('has_population', $9, $10)
                        ('=', $11, 1000000)
                        ('>', $10, $11)
                        ('contains', $8, $9)
                    ], 2)
            ])
    ]

183 msecs


So how to do it? Some options:

- wrap a `isolate({block})` relation around the independent part, so that is executed only once.

Works for [A]

    [
        ('ocean', $1)
        ('isolate', [
            ('borders', $1, $2)
            ('isolate', [
                ('african', $2)
            ])
            ('isolate', [
                ('country', $2)
            ])
        ])
        ('isolate', [
            ('borders', $1, $3)
            ('isolate', [
                ('asian', $3)
            ])
            ('isolate', [
                ('country', $3)
            ])
        ])
    ]

Could also work for [B], but `flows_from_to` should be placed up front.

    [
        ('resolve_name', 'Black_Sea', $6)
        ('flows_from_to', $5, $4, $6)
        ('isolate', [
            ('river', $5)
        ])
        ('isolate', [
            ('country', $4)
        ])
    ]

What would it do for [C]?


~~~python
    [
        ('continent', $7)
        ('none',
            [
                ('country', $8)
                ('isolate', [
                    ('in', $8, $7)
                ])
                ('isolate', [
                    ('det_greater_than',
                        [
                            ('city', $9)
                            ('isolate', [
                                ('has_population', $9, $10)
                                ('=', $11, 1000000)
                                ('isolate', [
                                    ('>', $10, $11)
                                ])
                                ('isolate', [
                                    ('contains', $8, $9)
                                ])
                            ])
                        ], 2)
                ])
            ])
    ]
~~~

Compare Chat-80's original plan:

~~~prolog
    answer([A]) :-
    A = setof B
        continent(B)
    & { \+
            exists C D
            in(C,B)
            & {country(C)}
            & { D = numberof E
                exists F
                    in(E,C)
                & {city(E)}
                & { population(E,F)
                    & {exceeds(F,--(1,million))} }
            & {D>2} } }
~~~


There is no need to isolate the last subquery in a group.


## 2024-08-17

I want to move away from Instances, and store facts about reified variables in a dialog store. Main reason: the instances with their types only work if all quantifiers occur before the other relations. It's completely outdated.

The dialog context is a memory store that contains facts about reified dialog variables.

I will distinguish between sentence contexts and dialog contexts. Sentence contexts are cleared at the start of every composition.

The sentence context is there because we don't want to pollute the dialog context db with facts that belong to discarded interpretations.

## 2024-08-10

I implemented Warrens query optimization algorithm (which is awesome!). It brought the time to run the queries from 50 seconds down to 0.46 seconds. That seems to be the best I can do. The large query now take 34 msecs. I don't think it can be done much faster in Python. Using Pypy it takes 20 msecs.

===

I added a simple inference module.

## 2024-08-08 a

I got this working. I am shocked how much more simpler I'm able to make the semantics using this new technique.

From

    [('find', E2, ('quant', E2, EXISTS, attr), vp_nosub_obj)]

to

    attr + vp_nosub_obj



## 2024-08-08

I was inspired by the simple logical constructs that Chat-80 creates. In comparison with them my own constructs were very heavy, and while they were simplified in the optimization step, it seemed strange to generate big structures just to be make them smaller afterwards. Also, I think it's good to have this simplification knowledge inside the grammar. It makes you aware of the differences.

Here are some tests I did. In my mind I switched from atom-based to function based and back several times. Function based almost won, because it's simpler and shows where the "Body" comes from. However, the variables in the functions can't be replaced and this proved to be a problem I couldn't fix. Also function based has functions within functions and that makes it look complicated from the start. I think I found a rather elegant atom based solution.

=====================================================================================================

CURRENT

{
    "syn": "s(E2) -> 'is' 'there' np(E1) preposition(E1, E2) 'each' nbar(E2) '?'",
    "sem": lambda np, preposition, nbar: [('find', E2, ('quant', E2, ALL, nbar), [('find', E1, np, preposition)])]
}

=====================================================================================================

ATOM BASED

def apply(atoms, body):
	return replace(atoms, "Body", body)

{
  "syn": "s(E2) -> 'is' 'there' np(E1) preposition(E1, E2) 'each' nbar(E2) '?'",
  "sem": lambda np, preposition, nbar: [('all', E2, nbar, apply(np, preposition))]
}

# np
{ "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar + Body },
{ "syn": "np(E1) -> det(E1) nbar(E1)", "sem": apply(det, nbar + Body) },
{ "syn": "np(E1) -> number(E1)", "sem": lambda number: [('=', E1, number)] + Body },

# det
{ "syn": "det(E1) -> 'any'", "sem": lambda: Body },
{ "syn": "det(E1) -> 'no'", "sem": lambda: ('det-none', Body) },
{ "syn": "det(E1) -> number(E1)", "sem": lambda number: ('det-number', Body, number) },
{ "syn": "det(E1) -> 'more' 'than' number(E1)", "sem": ('det_greater_than', Body, number) },

=====================================================================================================

FUNCTION BASED


{ "sem": lambda np, preposition, nbar: [('all', E2, nbar + np(preposition))]}

# np
{ "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
	lambda Body: nbar + Body },
{ "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
	lambda Body: det(nbar, Body) },
{ "syn": "np(E1) -> number(E1)", "sem": lambda number:
	lambda Body: [('=', E1, number)] + Body },


# det
{ "syn": "det(E1) -> 'any'", "sem": lambda:
	lambda Range, Body: Range + Body },
{ "syn": "det(E1) -> 'no'", "sem": lambda:
	lambda Range, Body: ('not', E1, Range + Body) },
{ "syn": "det(E1) -> number(E1)", "sem": lambda number:
	lambda Range, Body: ('det-number', E1, Range + Body, number) },
{ "syn": "det(E1) -> 'more' 'than' number(E1)", "sem": lambda number:
	lambda Range, Body: ('det_greater_than', E1, Range + Body, number) },
{ "syn": "det(E1) -> 'all'", "sem": lambda:
	lambda Range, Body: ('all', E1, Range, Body) },

PROBLEMS

strange to include Body in the meaning of an np, but makes sense
if "find" is gone, will "do" still work? (no but do is also not necessary, since all np's can be passed directly to a imperative verb)

=====================================================================================================

CURRENT BUT CHANGED

{
    "syn": "s(E2) -> 'is' 'there' np(E1) preposition(E1, E2) 'each' nbar(E2) '?'",
    "sem": lambda np, preposition, nbar: [('find', E2, ('all', Result, Range, nbar), [('find', E1, np, preposition)])]
}

{ "syn": "det(E1) -> number(E1)", "sem": lambda number: ('det_equals', Result, number) },
{ "syn": "det(E1) -> 'more' 'than' number(E1)", "sem": lambda number: ('det_greater_than', Result, number) },

=====================================================================================================

## 2024-08-03

By optimizing the in-memory data store, I brought processing time back from 50 sec to 8.1 sec; 7.8 seconds are spent by the complex (border-border-border) query.

===

Before starting to work on the borders-borders-borders I'll do this one first:

    Which country's capital is London?

It takes 83 msecs and that fast for the very inefficient way the sentence is executed.

~~~python
[
    ('country', S1)
    ('find', S2,
        ('quant', S2, 'exists',
            [
                ('capital', S2)
            ]),
        [
            ('of', S2, S1)
            ('find', S3,
                ('quant', S3, 'exists',
                    [
                        ('resolve_name', 'London', S3)
                    ]),
                [
                    ('==', S2, S3)
                ])
        ])
]
~~~

First we load all countries, then for each country, we find all capitals and remove the ones that do not belong to the country. Then still for each country, we resolve the name "London" and check if it is indeed the capital.

We need to transform this query into:

~~~python
[
    ('resolve_name', 'London', S3),
    ('==', S2, S3),
    ('of', S2, S1),
    ('country', S1)
]
~~~

Or some other simple representation that does the job.

The DEC KL-10 of Warren and Pereira ran at 50Mhz. My Lenovo LOQ 15IRH8 runs at 2000Mhz, which makes it 40 times faster. My machine has 12 cores, which I'm not using yet.

## 2024-08-02

In their papers, Warren and Pereira mentioned their query response times. They ranged from 200 to 800 msecs. I thought that was ok, and something I would be able to match easily. Only when I ran their system on a current computer it dawned on me how much processing speed has increased. Response times are now between 0 and 2 msecs. That includes parsing and execution! I had to change a sample sentence a bit to ensure myself that the results weren't just cached. There's much to be done before I can reach this speed. In fact, only the parsing in my system takes already a few msecs, to I will never be able to compete. I can merely do my best to come near... this is humbling.

===

I imported all actual data from Chat-80 from CSV files into the in-memory database and ran the tests again. In total they take now 50 seconds to run (!) This sentence, as expected takes up most time: 43 seconds.

    Which country bordering the Mediterranean borders a country that is bordered by a country whose population exceeds the population of India?

There are about a 1000 "borders" relations, they are bi-directional, and they are nested 3 times. Chat-80 runs even this question in less than 1 msec. *yaw drop*

This is what we're up against. Note that the query, in the time of Warren and Pereira, could have taken 12 hours, and the need to start optimizing would be essential.

===

I implemented this inference as part of the model

~~~prolog
contains(X,Y) :- contains0(X,Y).
contains(X,Y) :- contains0(X,W), contains(W,Y).
~~~

like this

~~~
out_values = self.ds.select("contains", ["part", "whole"], db_values)

part = values[0]
whole = values[1]
recurse = solver.solve([("contains", whole, E1), ("in", part, E1)], binding)
out_values.extend(recurse)
~~~

I plan to build a simple inference engine, to make these inferences easier. I will need them later.

## 2024-07-30

First pass of the Chat-80 dialog is complete. All questions have been answered. Leaving the functional approach and reverting to atom-based made it straightforward to complete the dialog. Answering all questions takes 0.3 seconds on my machine. But making it work is just one part of Chat-80. Chat-80 is really really fast. And I noticed that it also produces very simple semantic representations. So I need to:

* chat-80 import csv
* simplify semantics that uses EXISTS
* optimize: reorder atoms
* optimze: distinguish between all-quantors and existential quantors

===

After some profiling I found that the parser was currently taking most time. It could be optimized by moving the chart states into a set in stead of a list. Response time for all questions is now about 0.13 seconds.

## 2024-07-03

Next to "syn" and "sem", introduce "imp": the atoms that are implied by the sentence. May contain variables that should be turned into sentence variables. These implications can be used to deduce the intent of the sentence, but it can later also be used for other things. Their scope is currently sentence, but may later become dialog.

The implications need to be stored somewhere and be queryable just like other facts. Problem: you can assert atoms with free variables in the database. Answer: reification, turn a variable into a value (Instance("type": "variable, "value: "E1")). `category($E1, 'definiteness', 'definite')`, where `$` means: `reify`.

## 2024-06-25

Rewriting the functional execution approach to a relational (atom-sequence) approach.

While I was implementing `has child` again, making an exception for this verb "has", which needed to be mapped to `has_child`, it occurred to me that I don't have to do this in the grammar any more. The adapter can detect that the relation "has" is about a parent and a child, from the input values, and from this select the `has_child` table to query from. That's a nice insight!

## 2024-06-15

Looking for other semantics parsers, I checked Sippycup once more ( https://github.com/wcmac/sippycup ). I know I have seen this before, so it must have influenced this library, but it probably was in a time that I didn't program in Python yet.

Anyway, seeing it again came as a huge shock. Not so much that its approach is largely similar to the one this library takes, but the fact that it presents multiple ways to deal with semantics. Each of its tutorial pages has a different semantic representation.

In its third unit that deals with geographic queries https://nbviewer.org/github/wcmac/sippycup/blob/master/sippycup-unit-3.ipynb it takes the approach I have used here as well. The semantics of a rule consists of lambda functions, and these are combined to create the complete semantics.  So far so good.

The last few weeks I kept noticing how much easier it was to write semantics in NLI-GO, which uses a relational rather than a functional approach. And that previous approach had more advantages:

- as it iss declarative, it is data (atoms) and can be manipulated
- it can be used to store learned information. If the system has to learn a rule "all men are mortal", how is this knowledge to be persisted if it is in functional form?
- the atoms can be used to do generation
- the atoms can also be used to reorganize the semantics, as may be needed for scope resolution
- the atoms can be used to optimize the semantics for performance

At the same time I was rethinking my approach to database access. So far I worked with toy domains, and performance was not an issue. But one of the things I want the library to be able to do is answer questions like "How many customers have bought more than 2 products in the last month?" As this is about customers (let's say 10.000 and products (let's say 100.000), such a simple query would run my library to the ground immediately). The consequence is simple: I need my library to produce SQL / Sparql queries. It's the only way to reach any kind of performance. It's not all it should do, but it should be able to do it. And it should not produce SQL directly, it should do this based on the age old logical form: `(predicate arg arg)`, with nested arguments. It that possible?

===

It seems like that is very hard to do.

There are means of optimization. In stead of 10.000 x 100.000 queries, it's possible to do one query that leaves the relevant id's open. So this line of thought may not be as hopeless as it seems.

## 2024-06-09

What an impossible question ...

What are the continents no country in which contains more than two cities whose population exceeds 1 million?

What is the parse tree?

Let's check what Chat-80 itself produces...

~~~
whq
   B
   s
      np
         3+plu
         wh(B)
         []
      verb(be,active,pres+fin,[],pos)
      arg
         dir
         np
            3+plu
            np_head
               det(the(plu))
               []
               continent
            rel
               C
               s
                  np
                     3+sin
                     np_head
                        det(no)
                        []
                        country
                     pp
                        prep(in)
                        np
                           3+plu
                           wh(C)
                           []
                  verb(contain,active,pres+fin,[],pos)
                  arg
                     dir
                     np
                        3+plu
                        np_head
                           quant(more,nb(2))
                           []
                           city
                        rel
                           D
                           s
                              np
                                 3+sin
                                 np_head
                                    det(the(sin))
                                    []
                                    population
                                 pp
                                    poss
                                    np
                                       3+plu
                                       wh(D)
                                       []
                              verb(exceed,active,pres+fin,[],pos)
                              arg
                                 dir
                                 np
                                    3+sin
                                    np_head
                                       quant(same,nb(1))
                                       []
                                       million
                                    []
                              []
                  []
      []


~~~


## 2024-06-08

What are the countries from which a river flows into the Black_Sea?

This is a ditransitive verb phrase with subject and object reversed. I created a notation for the verb phrase that expresses both the order of the arguments and which ones are missing.

~~~python
    { "syn": "s -> 'what' 'are' np vp_noobj_sub_iob '?'", "sem": lambda np, vp_noobj_sub_iob: lambda: np(vp_noobj_sub_iob) },
    { "syn": "vp_noobj_sub_iob -> 'from' 'which' np vp_noobj_nosub_iob", "sem": lambda np, vp_noobj_nosub_iob: lambda obj: np(vp_noobj_nosub_iob(obj)) },
    { "syn": "vp_noobj_nosub_iob -> vp_noobj_nosub_noiob np", "sem": lambda vp_noobj_nosub_noiob, np: lambda obj: lambda sub: np(vp_noobj_nosub_noiob(obj)(sub)) },
    { "syn": "vp_noobj_nosub_noiob -> dtv", "sem": lambda dtv: lambda obj: lambda sub: lambda iob: dtv(sub, obj, iob) },
    { "syn": "dtv -> 'flows' 'into'", "sem": lambda: lambda sub, obj, iob: model.find_relation_values('flows_from_to', [sub, obj, iob]) },
~~~

To resume the semantics:

~~~python
lambda: np(vp_noobj_sub_iob)
lambda obj: np(vp_noobj_nosub_iob(obj))
lambda obj: lambda sub: np(vp_noobj_nosub_noiob(obj)(sub))
lambda obj: lambda sub: lambda iob: dtv(sub, obj, iob)
lambda sub, obj, iob: model.find_relation_values('flows_from_to', [sub, obj, iob])
~~~

There's beauty in this.

## 2024-06-05

Wow @

> Is there more than one country in each continent?

- per continent
    - find the countries in the continent
    - count them
    - more than one? yes / no
- are all of them yes?

The latter clause makes this sentence essentially different from the previous one. In stead of answering:

    Europe: yes
    America: yes
    Antartica: no

The expected answer is simply:

    No

===

These questions can benefit from the technique that an aggregate that fails is left out of the group by. In the previous question "Antarctica" was left out of Chat-80's results as it has no countries. If I leave don't add the continents to the group by that have no countries, I can answer the question by comparing the number of group-by elements with the number of continents. Not equal => "no".

The custom aggregation function could return `False` if it failed, or produced no results.

## 2024-06-04

An interesting sentence in Chat-80's dialog:

> What is the average area of the countries in each continent?

It expects an answer like

    Europe: 500.000
    North America: 700.000
    Australia: 400.000

It is what would be a GROUP BY in SQL: `SELECT continent.name, AVG(country.area) OF country JOIN continent GROUP BY continent.id`.

What does take to process it?

- in each continent
- collect the areas of the countries
- take the average of these areas

or

- collect all countries
- look up each country's area
- group by continent and average

Chat-80 does this:

- collect the continents
- collect the area per country
- average over the countries per continent

## 2024-05-31

The executionable meaning of the sentence "What is the ocean that borders African countries and that borders Asian countries?"

~~~python
lambda np: lambda: np()
    lambda det, nbar: create_np(det, nbar)
        lambda: exists
        lambda np, rc1, rc2: create_np(exists, lambda: range_and(np(rc1), np(rc2)))
            lambda: lambda: model.get_instances('ocean')
            lambda vp_no_sub: lambda subject: vp_no_sub(subject)
                lambda tv, np: lambda subject: np(tv(subject))
                    lambda: lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True)
                    lambda nbar: create_np(exists, nbar)
                        lambda adj, noun: lambda: adj(noun)
                            lambda: lambda range: model.filter_by_modifier(range, 'african')
                            lambda: lambda: model.get_instances('country')
            lambda vp_no_sub: vp_no_sub
                lambda tv, np: lambda subject: np(tv(subject))
                    lambda: lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True)
                    lambda nbar: create_np(exists, nbar)
                        lambda adj, noun: lambda: adj(noun)
                            lambda: lambda range: model.filter_by_modifier(range, 'asian')
                            lambda: lambda: model.get_instances('country')
~~~

## 2024-05-30

The big question was:

    np or np()

When creating grammar rules, should one use `np` (use the function) or `np()` (use the result of the function). I came up with the following rule:

1. If it is returned directly, use `np()`
2. If it is passed as an argument to a function, use `np`

## 2024-05-23

A relation is a combination of two or more entities of equivalent status. An attribute is a combination of two entities with subordinate status.

===

It _is_ possible to define a relation "of" without asserting an _attr_ category. And this involves en emphasis on the entities of the arguments:

    of(capital, country)

But going through all capitals just to find the capital of Greece is very inefficient, since it can be done with a simple lookup.

===

When looking for a relation, we can use the known entities as a retriction:

    capital of => of(capital, country)
    capital of => of(capital, state)

If `country` is known, this restricts the relations.

===

I think I'll introduce Range

    class Range:
        entity: str
        ids: list[str]

a combination of the entity ids with the name of the entity. I can use the entity to restrict things.

## 2024-05-22

I need to start thinking about events.

At some time you want to be able the question

    What was the capital of Greece in 1830?

===

I think I will leave events for the advanced section. Many projects can be done without events, and would complicate them. If you do events, you must do them everywhere, so this is something to consider at the start of a project. If will name this in the hints.

===

Think of deictic centers as contexts. If I could inject the current contexts (of time, place etc) into the dialog context, then I can inject it into the interpretation function as well. The advantage is that the grammar can stay simple, does not have to deal with time. Only the interpretation function then add time to the db query. Would that work?

## 2024-05-20

    What is the capital of Greece?
    Of which city is Athens the capital?

Relations between things. No good to iterate over all capitals.

I need a query that can be modified based on the context:

"capital of"

    select country_id, capital_id from country cn inner join city ci on ci.country_id = cn.id [where cn.id = 15]

"whose capital is"

    select country_id, capital_id from country cn inner join city ci on ci.country_id = cn.id [where ci.id = 15]

A relation expressing a verb, used by `find`, will need both where clauses

Only the where-clause changes.

## 2024-05-19

I added control blocks and release version 0.2.0. I'm renaming the good old `quantifier phrase` to `determiner` (not `dp`, because this has a different connotation).

## 2024-05-16

The database has an insert and a delete.
The domain has a select, but not insert and delete.

~~~python
domain = MyDomain([
    db1, db2
])
domain.select('has_child', {child=2}, 'parent')

class MyDomain
    def select(self, relation, where_clause, select_clause):
        if (relation == 'has_child')
            return self.db1.select()
~~~

or

~~~python
domain = Domain([
    { 'relation': 'has_child', fields: ['parent', 'child'], 'db': db1, 'map': "(parent, child) -> parent(parent, child) gender(child, 'male')"}
])

grammar = [
    { "syn": "child -> 'children'", "sem": lambda: lambda: domain.select('has_child', ['child']) },
    {
        "syn": "vp_no_sub -> aux qp child",
        "sem": lambda aux, qp, child:
                lambda subject: find(
                    (qp, child),
                    lambda object: domain.select('has_child', [subject, object])))
    },

]
~~~

what about this:

~~~python
mem_db = MemoryDb()

domain = Domain([
    Relation("has_child", ['parent', 'child'], lambda parent, child: mem_db.fetch_column('select 1 from has_child where parent_id = %s and child_id = %s')),
],
[
    EntityType("father", lambda: mem_db.fetch_column('select parent_id from has_child hc inner join gender g on ...')),
])
~~~


## 2024-05-15

I need a way to express a noun or adjective in a way that doesn't depend on a specific database or table, as in

    db.select(Record('has_child'))

It needs to be a separate level of abstraction, in order to

- make the grammar more reusable

I can add a new object Domain that accepts databases. One of the challenges is the mapping of knowledge level to db level. Most mappings are simple but here's a mapping that requires 2 relations:

    dom:has_son(A, B) :- parent(B, A) gender(B, 'male');

This code may be do the job:

    domain = Domain()
    domain.add(MemoryDb(), [
        { "rel": "has_child", "map": lambda r: r },

        { "rel": "has_son", "map": lambda r, db:
            db.select(Record('parent', {'parent_id': r.values['parent'], 'child_id': r.values['child']})).
            join(db.select(Record('gender', {'g': 'male'}), ['parent', 'person_id'])) }
    ])


## 2024-05-12

Passing `node` to the semantic functions made the semantics code __much__ more verbose. And more complicated too, because now the user needed to choose between using a function or a node. The benefit would mainly be handling the np.

When I found another way to handle the np I switched back to semantic composition. I don't execute the `qp` and `nbar` of the `np`, I just group them and pass the group as a value to the parent semantic. The semantics code is much shorter and readable for it.

I created a proof of concept using the sentence "each parent has two children". I needed a database-like structure for the sentence so I created a little in-memory "database".

This is now a typical parsing rule:

    {
        "syn": "s -> np vp_no_sub",
        "sem": lambda np, vp_no_sub: lambda: find(np(), vp_no_sub)
    },

The "syn" (for syntax) is the rewrite rule. "sem" is a plain Python function that takes the semantic functions of its (non-word) children as inputs and returns a function that acts on these child functions. The outer function declares the dependencies (the child semantics) and is executed by the composer to get to the inner function. The inner function then has access to the child semantics in its closure. It is the inner function that is passed as depenency to the parent semantic function.

Seeing this proof-of-concept work made me so enthousiastic that I set up a documentation repository `richard-readthedocs` and website https://richard.readthedocs.io/. I also created a package on the official Python repository PyPi. So we're now on version 0.1.0.

Note that I'm using a term like "vp_no_sub", rather than just "vp". I'm not sure about the wording, but creating variants of `vp` seems like a very good idea, if only because the semantic function of "vp" would take a different number of arguments than the "vp_no_sub", and use them differently.

Now I need to write documentation and work on testing and error handling.

## 2024-05-09

To handle quantification, have a look at this simplified representation

    S - check(np, vp)
    - np - quant(qp, nbar)
        - qp - every
        - nbar - parent
    - vp - has two children

The problem is that the function `check` needs direct access to the sem of `qp` as it needs to check if `vp` applies to (in this case) _all_ np's. `qp` however is not a direct child of `s`, but it's a _grandchild_`. Where NLI-GO could access the grandchild because of its declarative nature, Richard could not (at this moment).

Would it be possible to arrange the syntax so that it becomes a direct child?

    S - check(np, vp)
    - qp - every
    - nbar - parent
    - vp - has two children

In theory, yes, but it would split the NP over two nodes, which complicates things, and further, it seems that no linguistic theory has ever done that.

Giving a node access to the semantics of it's grandchild can be handled in a ridiculously simple way, by passing the parse tree node to the semantic function.

    sem: lambda node: check(
                        node.child_sem('np').child_sem('qp'),
                        node.child_sem('np').child_sem('np'),
                        node.child_sem('vp')
                    )

Note that this is a special case. Quantification is the only application that needs access to a grandchild that I know of.

Giving semantics access to the parse tree node, and hence to a bit of its syntactic and word form basis, can have added benefits. SHRDLU for example contains the interaction

    H: How many things are on top of green cubes?
    C: I'M NOT SURE WHAT YOU MEAN BY "ON TOP OF" IN THE PHRASE "ON TOP OF GREEN CUBES" .

Where the quoted phrases are taken literally from the input sentence, and would not be readily available to semantics in NLI-GO, for example. I'm not saying this is important, but it crossed my mind.

The other _big_ advantage of this method is that it requires no composition step.

## 2024-05-05

I started a new Github repository for this project and another one to create the "Github Pages" documentation site for it. I didn't know about this Github service but this is a good time to try it out.

## 2024-04-23

I started this new project because NLI-GO was too much bogged down in its self-created dual-aspect programming language. It caused hard problems every time and conflicted too much with the goal of being simple.

After some months of idling I had the idea of implementing semantics in the host programming language directly, as functions. In this case it's Go, but it should be any language that allows functions as terms and hence as arguments to other functions. This holds true for most modern languages. It seems to me the simple consequence of Richard Montague's writings, but strangly I can't find any example of such direct implementation of semantics when searching the web.

A few days ago I managed to manually create a single function, representing the meaning of the sentence "add 2 to 5" by combining the meaning-functions of the phrases of a sentence. That was an important proof-of-concept, but I need some more cases to be confident that this approach works.

One point of concern are long-term dependencies. I've used this sentence before and I will use it now:

    Which babies were the toys easiest to take from?

    s                                       sense: check($np, $dep_vp)
        which
        np(E1)                              sense: quant(_, some(_), E1, $nbar)
            nbar(E1)
                noun(E1) - babies
        dep_vp(P1, E1)                      sense: check($np, $advp $vp)
            be() - were
            np(E1)                          sense: quant(Q1, $qp, E1, $nbar)
                qp() - the
                noun(E1) - toys
            adv(P1) - easiest
            vp(P1, E1, E2) - to take from   sense: take_from(P1, E2, E1)

The core of this sentence's meaning is the `check($np, $dep_vp)` from `s`. It first collects all `$np` ("all babies"), then feeds these as arguments to `$dep_vp` ("were the toys easiest to take from").

I can do that also in the new system. Find all `np()`, then pass these as argument to `dep_vp()`. The result of the function would then be a list of baby-ids. But I'm wondering if it is okay that a `dep_vp` always returns the missing `np`. Could it be possible that the newly found `P1` is needed as well? Should the `dep_vp` return a list of bindings?

Where NLI-GO was like Prolog that relied on multiple variable bindings, Richard! uses function return values as meaning. This makes it quite a bit different, and I can't yet see all the consequences.

Next to being functional semantic, the new approach also uses intersection to form meaning (a "red car" is the set of cars that is the intersection of all red objects and all car objects).

Another point of concern: quants, consider:

    Do at least 5 babies play with a ball?

    s                                       sense: check($np, $dep_vp)
        np(E1)                              sense: quant(_, $qp, E1, $nbar)
            qp()                            sense: at least 5(E1)
            nbar(E1)
                noun(E1) - babies
        vp(P1, E2)                          sense: play(P1, E2)

To process `check($np, $dep_vp)`, the system needs to go through all `np`'s and then check if the requirement `qp` ("at least five") is met. In the `do()` variant, it needs to try the `np()`'s until `qp()` is met. Perhaps `np` should deliver an iterator?

    {
        /* "... I told you to pick up" */
        rule: vp_without_np(P1, L1) -> np(E1) meta_verb(P1, E1, E2, P2) np(E2) vp_without_nps(P2, E2, L1),
        sense: go:check($np1, go:check($np2, $vp_without_nps $meta_verb))
    }

`meta_verb` returns a set of bindings?

    "Does every parent have 4 children?"

    for every parent
        for exactly 4 children
            the parent has the child

    s
        does
        some_vp : check(np1(), check(np2, verb))
            np1
                qp1 : go:quantifier(Result, Range, $quantifier)
                    quantifier - every : [Result == Range]
                nbar parent
            verb
            np2
                qp1 : go:quantifier(Result, Range, $quantifier)
                    quantifier - 4 : [Result == 4]

                nbar children


    func check()


Richard! doesn't translate from syntax to logic, instead it just uses functions for semantic composition, and adds custom code to each node. This custom code executes the sentence (imperative) rather than just forms a logical expression. The parsing is functional, but the semantics is imperative.

