## 2026-02-24

Some thoughts: a "sense" is the informational essense of things. It has a dual nature: can take the form of a variable in questions and of a constant in statements. Apart from that it is also a pointer, which can point to other senses with which it identifies, and to itself. In questions and statements it is "fluid", in statements it is "solid". It has a name, which is unique within a dialog.

Common entities like I and You can have a fixed dialog constant.

Could it be that is needs to be both solid and fluid in the same sentence? I need to check some statements to see whether this may be the case. And if so, how can i refine the fluid/solid distinction?

Willa was hungry. She picked up the Michelin guide. She got into her car.
name(D1, Willa) hungry(D1)
she(D2) michelin_guide(D3) pick_up(D2, D3)
she(D3) car(D4) get_into(D3, D4)
=> okay

A "steeple" is a stack which contains two green cubes and a pyramid.
name(D1) stack(D1) cube(D2) two(D2) green(D2) pyramid(D3) and(D4, D2, D3) contain(D1, D4)
=> you can't use this definition to match new objects, because of the lack of variables
=> at the same time, this definition lends itself to be declared by variables

I own blocks which are not red, but I don't own anything which supports a pyramid
=> needs variables to be used to check if I own something
=> is stored in a rule

The decision to use variables or constants can be left to the intent.

===

Interestingly, In "Cooper" I already used constants (or reified variables) to store facts in the dialog context. But it needed two grammars: a write grammar and a read grammar. "SIR" also stores information, but its facts are very simple and based on names.

## 2026-02-23

I need dialog entity identifiers. Variables seem to be a solution, but how to reason about them? Wouldn't you need variables that have variables as values? This is confusing. So you want dialog identifiers. Real values. That represent entities in the dialog. These may be single individuals or groups. They may be unidentified yet. Just roles, really. But not variables.

Can I distribute dialog identifiers for each entity in the dialog?

    John likes Mary
    name('D1', 'John') name('D2', 'Mary') likes('D1', 'D2') -> okay

    what countries have more than 5 million citizens?
    country('D1') citizens('D1', 'C1') greater('C1', 5M) -> not possible

The difference between these is that one is a statement (introduce ids), while the other a question (use variables). Can it be like that?

How is it that Discourse Theory is to represent relationships using variables?

The problem with the dialog ids is that you can't equate ids, while you can equate variables. However, this may not be a real problem. If you can equate variables, you may as well equate ids. You just have to allow one id to point to another id.

## 2026-02-21

- check online if you can find WAM's algorithm for unification
    - An Abstract Prolog Instruction Set - David HD Warren (1983)
    - Well, okay, this to way too much different to be of use
- new unication
    - remove unbound_arguments
    - all arguments are dereferenced, so we're passing values down the line as much as possible, and this is ok, once a variable has a value, the value is all that matters
- it's no longer necessary to pass `bindings` in the solving process. `arguments` is enough (!)

## 2026-02-19

That change is not trouble free. Multiple tests fail in ways that are not easily fixable. I will first concentrate on building more unit tests.

## 2026-02-15

I implemented the unification of unbound variables. But I haven't worked out the effects of this unification on the execution of atoms yet.

## 2026-02-14

The idea of unification of unbound variables I got from "From discourse to logic" by Kamp and Reyle.

===

Now, *if* I use variable unification to solve the anaphora problem, what would that look like? Keep in mind that the CD folks claim that anaphora resolution is almost a non-problem.

Let's see. Start with 

    Willa was hungry 
    ('name', $2, 'Willa'), ('hungry', $2)

then we get 

    She picked up a Michelin Guide 
    ('name', $4, 'She'), ('michelin_guide', $5), ('pick_up', $3, $4, $5)

How do we get $2 and $4 to be the same entity?

First PAM goes through a number of induction iterations:

    ['take-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
    ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['poss', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]]]],
    ...
    ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [0]]]]]]],

all these just apply to the variables of the second sentence.

But then comes a `predicted` step: "Confirms prediction from", matching the rule

    [
        [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
        [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]]
    ],

Now the new goal deduced from the second sentence matches the first sentence. In my lingo this would say (something like):

    ('goal', ('not', ('hungry', E1))) => ('hungry', E1)

The antecedent matches the second line, whicle the consequent matches the first line. The unification of both creates a link between their variables.

And thus: $2 = $4

QED

## 2026-02-13

I asked ChatGPT for a basic algorithm for unbound variable unification in Prolog. This is what it returned:

~~~

unify(X, Y):
    X = deref(X)
    Y = deref(Y)

    if X == Y:
        succeed

    else if X is unbound variable:
        Heap[X] = Y
        succeed

    else if Y is unbound variable:
        Heap[Y] = X
        succeed

    else if both are integers:
        succeed if equal, else fail

    else:
        fail
 
~~~

When asked what was the source of the algorithm, it said that it created the algorithm itself, based on multiple sources.

The algorithm is brilliant in its simplicity. I understand it now, and I've written a blogpost about it:

https://patrick-van-bergen.blogspot.com/2026/02/unbound-variable-unification-in-prolog.html

## 2026-02-12

Working on fact induction. I created a separate predicate (`induce_facts`) that can be used in an intent to derive new facts from a given input. The predicate can use induction rules like this:

    name(E1, "Willa") => female(E1), person(E1).

The left hand side (antecedent) can have multiple conditions.

===

Based on the input `[('name', $2, 'Willa'), ('hungry', $2)]` I can now induce new facts. But first the variables of the input need to go.

[('name', $2, 'Willa'), ('hungry', $2)]
[('she', $4), ('michelin_guide', $5), ('pick_up', $3, $4, $5)]
[('she', $7), ('car', $8), ('her', $8), ('get_into', $6, $7, $8)]

* I used to resolve the id's of names and pronouns as the atoms were executed
* now they are not executed
* maybe I should execute the code, just for the sake of resolving the id's
* no resolving an atom like `hungry($2)` just fails
* maybe a new mode, next to the `query mode`, an `assert mode`, that first tries to query each atom, and if that fails, store the atom
* that will not help me resolve pronouns
* I think PAM just uses the name "Willa" as an identifier, which is possible within a single story
* Another take: just change variabe $2 to string `$2` and store it. The stored string `$2` is *still a variable*. The reified version of the variable. Why's that important? Because we can later store `$2 = $3`. This unification of variables is allowed in Prolog.
* Gemini: "In Prolog terms, when two unbound variables are unified, they become aliased. They don't just "point" to the same value; they become different names for the same logical memory cell."
* for today: take the atoms, reify them, and store them in memory. later, unify the reified variables
* how?
* there are 2 problems:
* how does the variable unification work
* when is the unification performed?
* a=b, d=c, b=c; a->b, d->c, b->c
* a=b, b=c; a->_1, b->_1, c->_1
* a=b, c=d, b=c; a->_1, b->_1, c->_2, d->_2, _1->_2
* create a variable indirection table: [variable-from, variable-to]

## 2026-02-10

I'm now in the grip of tree-structures. Let's have a look

Tree-representation of the same sentence:

{thought
    sub: {name: "John"}
    obj: {like: {
        sub: {name: "Mary},
        obj: {reference: "him"}
    }}}

Let's take a sentence with a quantifier:

"What is the average area of the countries in each continent?"

{is
    sub: E1,
    obj: state {
        type: area
        modifier: average,
        obj: country {
            in: continent
        }
    }
}

or

{is
    sub: E1,
    obj: average_area {
        obj: country
        group: continent
    }
}

===

On the other hand, there's a sliding scale from tuples to objects:

    person(E1, Name)
    person(id=E1, name=Name)
    person {
        id: str
        name: str
    }

===

Willa was hungry

['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],

(is,
    actor { person { name = "Willa" }},
    state { hunger { val = 5 }}
)

Willa was in a state of hunger

(state, 
    E1,
    hunger
)

The actor named Willa was in the state of hunger

(is, 
    actor: E1,
    state: hunger
)

A was B

(is, 
    actor: [],
    state: []
)

(is, 
    name("Willa"),
    hunger()
)

===

But, placing this in the database:

[('name', '$2', 'Willa'), ('hungry', '$2')]

also allows me to use `('hungry', '$2')` as a condition for a rule.

===

The rule

    [['take-plan', ['planner', '?x'], ['object', '?y']]],
    [['grasp', ['actor', '?x'], ['object', '?y']]]

can also be written as

    grasp(E1, E2) => take_plan(E1, E2)

===

Can I turn the `PlanAnalyzerModule` into a `InductionModule`? It could then allow for bot plan analysis, and basic induction, both of which are used by CD and PAM. The former is more specific PAM, the latter is general CD (in fact it's part of the CD parsing process).

## 2026-02-09

I'm trying to find out how to store second order sentences. So far I'm using id's to represent events and to create second order representations. This works well as a means to store relations, but it doesn't work at all as a means to query the second order data. I now need to store sentences, goals, plan instances, etc. 

What about storing second order events like this

"John thought mary liked him very much"

name(E1, "John") name(E2, "Mary") think(E1, 
                                    like(P1, E2, E1) very_much(P1))

I added "very much" to ensure to predicate on the event itself. Still needing the extra variable.

With this representation, it is no longer possible to just ask "Does Mary like John?"

## 2026-02-08

Storing sentences as relations in a relational database makes no sense. I need to later recall the sentential structure and this is lost once it's in the database.

===

My first sentence "Willa was hungry" reads

    ('name', '$2', 'Willa') ('hungry', '$2')

It's very unlike

    ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]]

and it doesn't have the predicate `is` to recognize it as a theme.

For now I store the sentences in arrays, just as MicroPAM does. If a sentence (semantic structure) does not have a `goal` or `plan` atom, it's stored as a theme.

===

Relational databases are only useful for very simple knowledge structures: is, has. Time-related is still possible, but second order knowledge is very problematic. Possible, of course, but not a good fit.

=== 

I asked Gemini for a database to store second order knowledge and it recommended Neo4j. I can look into this later. This only becomes relevant with large amounts of data.

===

Second sentence: "She picked up the Michelin guide".

This is the first rule to find:

    [
        [['take-plan', ['planner', '?x'], ['object', '?y']]],
        [['grasp', ['actor', '?x'], ['object', '?y']]]
    ],


## 2026-02-06

What is the answer to the question "Why did Willa pick up a Michelin guide?"?

- to go to a restaurant
- to find out the location of a restaurant
- to know the proximity to a restaurant
- to read the restaurant guide
- to possess the restaurant guide


    ['do-$restaurant-plan', ['planner', ['person', ['name', ['Willa']]]], ['restaurant', 'restaurant']],
    ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['prox', ['actor', ['person', ['name', ['Willa']]]], ['location', 'restaurant']]]],
    ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['know', ['actor', ['person', ['name', ['Willa']]]], ['fact', ['is', ['actor', 'restaurant'], ['prox', None]]]]]],
    ['read-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
    ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['poss', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]]]],
    ['take-plan', ['planner', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
    ['grasp', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
    ['goal', ['planner', ['person', ['name', ['Willa']]]], ['objective', ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [0]]]]]]],


## 2026-02-05

I might as well start PAM with the story from MicroPAM

    Willa was hungry
    She picked up the Michelin guide
    She got into her car

But what would be a good question to ask?

    Why did Willa pick up a Michelin guide?
    Why did Willa get into her car?
    Where did Willa drive to?

===

Is the decomposition of meaning (as in CD) essential to the recognition / matching of rules?
Is the hierarchical semantic structure (as in CD) essential.

I must say I'm intriguiged by the tree structure I saw. Systems like CHAT-80 use semantic structures that are as flat as possible as that's the only way it can optimize for querying efficiency.

The hierarchical structure seems essential to modal verbs like "may" and "can" and for second order verbs like "think".

Here again we may want to allow multiple representations of the same sentence. Some reps are better for database querying, some are better for rule matching.

On the other hand, a flat representation may do just as well. 

Let's just start with what I have and check again when I run into a problem.

## 2026-02-03

I created a separate repo for the MicroPAM port: https://github.com/garfix/micropam

===

The `chain` of MicroPAM is a bit problematic. It is a stack where "cd's" (facts) are added and removed in a seemingly unorganized way. Each time a cd was not predicted, it is added to the chain. Then, when inferences are tried, the top cd is popped. New cd's are pushed whenever a new inference can be made. So it's hard to say what the chain contains at the end, when all cd's are written to the database. Some inferred facts will be missing. Perhaps these are mere intermediate inferences, but who can tell that these facts are not important when a new sentence of the story is added? It could be that a new sentence was predicted by these facts. Is the omission intentional. Maybe, but it seems impossible to keep this in mind when developing a system. It seems like an uncertain business, and possibly wrong.

Also, PAM distinguishes between themes, goals, and plans. MicroPAM however, hardly distinguishes between them. They're all treated alike. And this begs the question if it's worthwhile to make this distinction in a working system. Is the added complexity necessary?

## 2026-01-31

Apparently the CD representation is fundamentally tree-like. Every sentence so far has a single top-level predicate, such as "PTRANS". Interesting!

## 2026-01-26

Start the implementation of MicroPAM.

## 2026-01-25

While I'm having trouble storing stories in relational form, it occurred to me that PAM may not store the literal information at all. It may just store all its inferences.

I added a check to ensure systems don't try to store variables in the database. This exposed an occurrence in Cooper, where exactly that had happened. I fixed it.

I have a language processor that is used to understand multiple languages in a single system. It just occurred to me that you can understand multiple languages by just combining all their rule sets. This has the added benefit that you can also add "uitdrukkingen uit een andere taal" within a sentence!

I removed the blocks from the code. They have irritated me from the start and I notice that the configuration tends to remain the same. The blocks make things unnecessarily complicated. 

The `System` makes place for `BasicSystem`.

This does mean that the quirky "Calculate three plus four times two" tests goes as well.


## 2026-01-22

I added a "SimpleFrameDataSource" that allows any data structure including nested tuples and lists. I'm not sure I need it, but it can always be handy to have.

It required a code rewrite: before, I passed None values to database routines, now I pass in variables, because the frame data store needed this.

## 2026-01-19

Converting Wilensky's data structures to something I would make myself is very hard. I will need to learn a new way of thinking.

I may need to create something of a frame-store, that stores frames. Like an Object DB? In order to store the goal and plan structures PAM builds.

Any data structure can be stored in a relational DB, but sometimes another data store is better suited. (CYC documentation also emphasis this)

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

A possible solution is to pull query optimization out of the ComposerModule and into specialized functions. Taking a Chat80 example:

~~~js
intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    store(output_type('list'), output_list(Elements)).
~~~

will become

~~~js
optimize(SemIn, SemOut) :- optimize_names_first(SemIn, Sem2), optimize_sort_by_cost(Sem2, Sem3), optimize_isolate(Sem3, SemOut).

intent_list(E1, Sem) :-
    optimize(Sem, SemOpt)
    find_all(E1, SemOpt, Elements),
    store(output_type('list'), output_list(Elements)).
~~~

---

Note that the idea of **intents** as predicates makes this kind of thing easy. If the intent is to query, then optimize the semantics first!

---

`optimize_isolate` needed the root variables (return variables) of the sentence. For this reason I added the SemanticSentence to the `ExecutionContext`. I also think I may need the current sentence later on; but on the other hand I'm a bit apprehensive to give this context to much information.


## 2026-01-17

I implemented unification (for example: `Atoms = lost(A)`), to make it easier to work with atom type variables.

---

It occurred to me that the SemanticComposer produces multiple versions of semantic representations, and that so far, only the last production is used by the rest of the system. However, the last production is mainly interesting for querying. It contains scoped constructs that are great for querying, but not so good for sentence analysis, such as I need for the PlanAnalyzer. Therefore it would be good to keep producing different versions of semantics, but to expose all of them for further processing.

## 2026-01-06

I'm starting the implementation of PAM with the example from chapter 14. First step: implement FIND-OUT-REQ: based on the sentence "John was lost", the system deducts that John will want to find out where he is. That is: a goal deduction rule.

## 2026-01-01

I asked Gemini for help on whom to contact for the original PAM source code. It suggested Christopher Riesbeck, one of the earliest members of the group around Shank. So I emailed him to help me find the source code. He responded by saying he didn't have any code left from that era, and that he'd also asked around. This means that I will have to re-invent the rules used to describe all domain knowledge, but at least I know that the code is not just accessible in an easy to find place. Riesbeck is also a coauthor of the book "Inside Computer Understanding: Five Programs Plus Miniatures", which contains a "micro implementation" of a.o. the PAM program. I ordered it from Amazon.

As input for PAM is complete stories, and yet they are processed one line at a time, I need the parser to be able to return multiple parse trees for a single piece of text. The parse trees it returned before are ambiguous variants. Each of these variants will now consist of multiple trees.
